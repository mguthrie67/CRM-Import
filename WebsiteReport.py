#!/usr/bin/python

dev=False
dev=True

##### TODO
###
### Option on webpage to add to spiders
### Read spiders from a file
### Weekly option to slowly rebuild known IP info
### Fix format on when

import gzip
import time
import shlex
#from urllib2 import urlopen
#from contextlib import closing
import urllib
import json
import socket
import smtplib
import operator
import os.path
from datetime import date, timedelta
from optparse import OptionParser

# Test settings
to={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}
frm={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}

# Prod settings
#to={"name" : "Reports", "email" : "reports@17ways.com.au"}
#frm={"name" : "What's Going on on the Web", "email" : "reports@17ways.com.au"}

class ApacheReader():
##########################################################################
# Class to handle opening, reading and interpreting the Apache log file  #
##########################################################################


##########################
# init                   #
##########################
    def __init__(self, IPHandler):

        self.IPHandler=IPHandler      # requests to resolve IP are sent to a handler class

# set up constants

        self.include=[".php", ".html", "GET / HTTP/"]
        self.spiders=["spider"]
        self.spiderhosts=["spider", "googlebot", "msnbot"]
        self.us="122.109.192.180"

# counters

        self.spiderscnt=0
        self.uscnt=0

# big lists

        self.visitlist=[]           # all the visits we care about - main hits on pages not from us or web crawlers
        self.visitors={}            # mapping of IP to relevant information on visitor
        self.visitorcount={}        # mapping of IP to count of pages visited
        self.visitorwhat={}         # mapping of IP to pages visited
        self.pagesvisited={}        # mapping of page name to IP addresses that visited it
        self.newvisitor=[]          # visits from people we haven't seen before
        self.countries={}           # mapping of country codes to a list of IPs from there

###########################
# load the file           #
###########################
# considering this started as 2 one line functions and I thought I didn't need them, its ended up as fucking mess

    def loadfile(self, range):

        self.range=range

        #print "RANGE----" + self.range

# we either get a value for range or we don't. If we do then it can be
# range = today             - use today
# range = dd/Mon/YYYY       - use date provided
# range = all               - provide all data for the files we have
# range = None              - when we get a value but we don't

# 2 are dates, one is everything, one is default, so lets flag them

        if self.range=="all":
            self.callflag="all"
            print "FILE - ALL"
        elif self.range=="today":
            print "FILE - TODAY"
            self.callflag="today"
        else:
            print "FILE - DATE"
            self.callflag="date"

# open the file - we need to use 2 files and stitch them together
# the archive file may contain data from yesterday and so may the live file
# ~/logs/17ways.com.au-<Month>-<Year>.gz is the archive
# ~/access-logs/17ways.com.au is the current file, seems to be rolled about 2pm, not zipped

# Date stuff
        if self.range==None or self.range=="all":
            yesterday = date.today() - timedelta(days=1)    # in hindsight yesterday was a bad choice of variable name!
# the month and year yesterday
            MonthYear=yesterday.strftime('%b-%Y')
# the date yesterday
            self.yest=yesterday.strftime('%d/%b/%Y')

        elif self.callflag=="today":
            yesterday = date.today()                        # too true!
# the month and year today
            MonthYear=yesterday.strftime('%b-%Y')
# the date yesterday
            self.yest=yesterday.strftime('%d/%b/%Y')

        elif self.callflag=="date":                          # specific date
# the month and year provided
            bits=range.split("/")
            MonthYear="%s-%s" % (bits[1], bits[2])
# the date provided
            self.yest=self.range

        print "Done that. Date is " + self.yest

# File stuff
        self.archivefile="/home/wayscoma/logs/17ways.com.au-%s.gz" % MonthYear
        self.livefile="/home/wayscoma/access-logs/17ways.com.au"

        if dev:
            self.archivefile="17ways.com.au-%s.gz" % MonthYear
            self.livefile="17ways.com.au"


# start with the archive file
        self.file=self.archivefile
        print "Opening " + self.file
        self.filehandle=gzip.open(self.file)


############################
# return next line of file #
############################
    def getnext(self):

        line=self.filehandle.readline()

# if we get false returned (EOF) then if it is the archive file, switch and open the live file
        if not line:
            print "Hit EOF on " + self.file
            if self.file==self.livefile: # already switched
                print "Already switched"
                return(line)
            else:
                print "Switching"
                self.filehandle.close()
                self.file=self.livefile
                self.filehandle=open(self.file)
                print "Opening " + self.file
                line=self.filehandle.readline()

# easy option - if all was specified just give it
        if self.callflag=="all":
            return(line)

# First time through we need to fast forward to yesterday
    #    print line
        datebit=line.split()[3]   # gives us [07/Jun/2015:16:38:22
        datepart=datebit[1:12]    # gives us 07/Jun/2015

        print "datepart: %s yesterday: %s" % (datepart, self.yest)

        if datepart==self.yest:   # valid date
            return(line)
        else:                     # not a valid date - keep reading until EOF or valid date
            while line:
                line=self.filehandle.readline()
                if line:
                    datebit=line.split()[3]
                    datepart=datebit[1:12]
                    print "Looking...found: %s looking for %s" % (datepart, self.yest)
                    if datepart==self.yest:    # found a valid one!
                        return(line)
# if we get here we have hit EOF without getting a valid date. We are either reading the live file so ok
# or there were no hits in the archive for yesterday in which case we will miss all of the live file data
# doesn't seem likely unless they change the time they roll the logfiles

# Except... if we are looking for today

                    if self.callflag=="today":
                        print "Switching - special case"
                        self.filehandle.close()
                        self.file=self.livefile
                        self.filehandle=open(self.file)
                        print "Opening " + self.file
                        line=self.filehandle.readline()    # must be today
                        return(line)

            return(False)

######################################
# process file and build information #
# main loop.                         #
######################################
    def dostuff(self):
        line=self.getnext()
        while line:
            self.processline(line)
            line=self.getnext()

# now we have read the file and built a list of the visits that we care about in visitlist
# visitlist is actually a list of every visit, so use this to build some other useful
# lists and dictionaries

#######
# go through the list of visits and update various things
#######
        for x in self.visitlist:

####
# Main mapping of visitor IP to details
####
            if not self.visitors.has_key(x['ip']):
                self.visitors[x['ip']]=self.IPHandler.getLocation(x['ip'])   # get details on this IP
   #             del self.visitors[x['ip']]['url']
    #            del self.visitors[x['ip']]['request']
     #           del self.visitors[x['ip']]['referrer']
     #           del self.visitors[x['ip']]['rc']
      #          del self.visitors[x['ip']]['when']

####
# Number of visits
####
            if self.visitorcount.has_key(x['ip']):
                self.visitorcount[x['ip']]=self.visitorcount[x['ip']]+1
            else:
                self.visitorcount[x['ip']]=1

####
# Pages visited by each IP      visitorwhat["1.2.3.4"]["Homepage"]==3  is 3 visits to homepage
####
            if self.visitorwhat.has_key(x['ip']):
                if self.visitorwhat[x['ip']].has_key(x['url']):
                    self.visitorwhat[x['ip']][x['url']]+=1
                else:
                    self.visitorwhat[x['ip']][x['url']]=1
            else:
                 self.visitorwhat[x['ip']]={}
                 self.visitorwhat[x['ip']][x['url']]=1

####
# pages by number of visits
####
            if self.pagesvisited.has_key(x['url']):
                self.pagesvisited[x['url']]+=1
            else:
                self.pagesvisited[x['url']]=1
#####################################
# process each line                 #
#####################################
    def processline(self, line):


# format the line
        parts=shlex.split(line)

    # Should give us

        ip=parts[0]
        request=parts[5]
        rc=parts[6]
        referrer=parts[8]
        agent=parts[9]
        when=parts[3][1:]

# get the hostname
        hostname=self.IPHandler.getLocation(ip)["hostname"]

    # is this a line we care about - only follow main entry points, not pictures etc
        relevant=False
        for x in self.include:
            if request.find(x)>=0:
                relevant=True
                break

    # ignore spiders
        spider=False
        if relevant:
            for x in self.spiders:
                if agent.find(x)>=0:
                    spider=True
                    self.spiderscnt+=1
                    break

            if spider==False:
                for x in self.spiderhosts:
                    if hostname.find(x)>=0:
                        spider=True
                        self.spiderscnt+=1
                        break

            if spider==False:
                url=request.split()[1][1:]
                url=url.replace("%20"," ")
                if url=="" : url="homepage"
                if url=="index.html" : url="homepage"

    # add our stuff
                stuff={}
                stuff["url"]=url
                stuff["ip"]=ip
                stuff["request"]=request
                stuff["rc"]=rc
                stuff["referrer"]=referrer
                stuff["agent"]=agent
                stuff["when"]=when

                if ip==self.us:
                    self.uscnt+=1
                else:
                    self.visitlist.append(stuff)



    def dataTotalVisitors(self):

# we want this sorted by number of visits

        sorted_x = sorted(self.visitorcount.items(), key=operator.itemgetter(1), reverse=True)

        return(sorted_x)


    def dataTotalPages(self):

# we want this sorted by number of visits

        sorted_x = sorted(self.pagesvisited.items(), key=operator.itemgetter(1), reverse=True)

        return(sorted_x)


class IPLookup():
#########################################################
# this class manages the lookups of IP addresses        #
# Get information about the visitor from the ip address #
#########################################################

############
# init     #
############
    def __init__(self):
        self.iplist={}        # keep a list of resolved addresses so we don't hit the server unnecessarily and get banned

# load from file - look at this later - maybe add a timer or throttle it
        if os.path.isfile("iplist.txt"):
            self.iplist=json.load(open("iplist.txt"))


#
#
# Add code to load this from a dump file except for once a week
# Also to save the in memory list - means we can report on new visitors too
#
#


###################
# lookup function #
###################
    def getLocation(self, ip):

# check if we already know this one

        if self.iplist.has_key(ip):
            return(self.iplist[ip])

        print "New lookup"
        print "######"
        print ip
        print "#######"

    # Get location info
        url = "http://ip-api.com/json/%s" % ip
        response = urllib.urlopen(url);
        data = json.loads(response.read())

# lookup DNS
        try:
            dns=socket.gethostbyaddr(ip)
            hostname=dns[0]
            alias=dns[1]
        except socket.herror:
       #     print "Lookup failed"
            hostname="unknown"
            alias=""

# add to data
        data["hostname"]=hostname
        data["alias"]=alias

# check it worked
        if data["status"]=="fail":
            data["city"]="Unknown"
            data["isp"]="Unknown"
            data["zip"]="Unknown"
            data["countryCode"]="Unknown"
            data["country"]="Unknown"
            data["region"]="Unknown"
            data["lon"]="Unknown"
            data["alias"]="Unknown"
            data["as"]="Unknown"
            data["lat"]="Unknown"
            data["timezone"]="Unknown"
            data["org"]="Unknown"
            data["regionName"]="Unknown"
            data["lat"]="Unknown"

        #print json.dumps(data)

#        for x in data.keys():
#           print "%s     : %s" % (x.strip(), data[x])

# add to list
        self.iplist[ip]=data

        return(data)




    def save(self):
        json.dump(self.iplist, open("iplist.txt", "w"))

##############################################
#                                            #
#                                            #
#            Generate the report             #
#                                            #
#                                            #
##############################################
class Report():

   global frm, to

   def __init__(self, c, range):

      self.data=c

      self.message=""

# Basic heading stuff for the email.
      day=time.strftime("%A")

# Check how we were run

      if range==None:     # normal use yesterday's date
         tits="Website Daily Report - %s" % day
         tits2="Website Report - %s" % day
      else:
         tits= "Special Report"
         tits2="Special Report"

      self.message+="""From: %s <%s>
To: %s <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: %s

<html>
<head>
<style>
body {
	font-family: 'Calibri','Verdana', 'Arial', sans-serif;
	background: #white;
	font-color: #blue;
}

h1 {
	font-size: 300%%;
    color:#5d73b6
}

h2 {
	font-size: 140%%;
}

h4 {
    color: #1F3D99;
    font-style: italic;
}


table.nice {

	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
    line-height: 6px;
}
table.nice th {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
    line-height: 8px;
}
table.nice td {
	border-width: 1px;
	padding: 6px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
	text-align: right;
}


a {
    text-decoration: none;
}
a:link, a:visited {
    color: #091e5e;
}
a:hover {
    color: #5d73f6;
}
</style>
</head>
<body>

""" % (frm["name"], frm["email"], to["name"], to["email"], tits)

      self.message+="<table width=100%%><tr><td><img width=120px src=http://17ways.com.au/images/logo_slogan.png>"
      self.message+="<td valign=middle><font size=96 color='#5d73b6'>%s</font></tr></table><hr>" % tits2
      self.message+="Who has been on our website. <a href='http://17ways.com.au/tools/WebDaily.html'>View as webpage.</a><br>"

      self.message+=self.printVisitors()
      self.message+=self.printPages()
      self.message+=self.printVisitorsDetails()

# Finish
      self.message+="</body></html>"

      self.message=self.message.encode('ascii', 'ignore').decode('ascii')

# Write webpage

      webfile="/home/wayscoma/public_html/tools/WebDaily.html"
      if dev:
        webfile="WebDaily.html"
      f=open(webfile, "w")
      for line in self.message:
         f.write(line)
      f.close()

# send email
      if not dev:
          smtpObj = smtplib.SMTP('localhost')
          smtpObj.sendmail(frm['email'], [to['email']], self.message)

   def printVisitors(self):
      x=self.data.dataTotalVisitors()
      msg="<h2>All Visitors</h2>\n"
      msg+="Excluding %s robots and us (%s).<br><br>\n" % (self.data.spiderscnt, self.data.uscnt)
      msg+="<table class='nice' border=1>\n"
      msg+="<tr><th>Hostname<th>Org<th>Timezone<th>Pages Viewed</tr>\n"
      for (ip, times) in x:
         msg+="<tr><td><a href=#%s>%s</a><td>%s<td>%s<td>%s</tr>\n" % (ip, self.data.visitors[ip]['hostname'], self.data.visitors[ip]['org'], self.data.visitors[ip]['timezone'], times)
      msg+="</table>\n"

      return(msg)

   def printVisitorsDetails(self):
      x=self.data.dataTotalVisitors()
      msg="<h2>Visitors Details</h2>"
      for (ip, times) in x:
          msg+="<br><hr>\n"
          msg+="\n\n<h3 id='%s'>%s</h3>\n" % (ip, ip)

# table of details
          msg+="<table class='nice' border=1 width='80%'>\n"
          msg+="<tr><th width='30%'>Attribute<th width='70%'>Value</tr>\n"
          y=self.data.visitors[ip]
          for k in y.keys():
             msg+="<tr><td width='30%%'>%s<td width='70%%'>%s</tr>\n" % (k, y[k])
          msg+="<tr><td width='30%%'>Location<td width='70%%'><a href='https://www.google.com.au/maps/@%s,%s,15z'>Google Maps</a></tr>\n" % (y['lat'], y['lon'])

          msg+="</table>\n\n"

          msg+="<br><br>\n"

# table of pages visited
          msg+="<table class='nice' border=1>\n"
          msg+="<tr><th>Pages Visited<th>Count</tr>\n"
          y=self.data.visitorwhat[ip]
          for k in y.keys():
             msg+="<tr><td style='text-align:left;'>%s<td>%s</tr>\n" % (k, y[k])
          msg+="</table>\n\n"

      return(msg)


   def printPages(self):
      x=self.data.dataTotalPages()
      msg="<h2>All Pages</h2>\n"
      msg+="Excluding %s robots and us (%s).<br><br>\n" % (self.data.spiderscnt, self.data.uscnt)
      msg+="<table class='nice' border=1>\n"
      msg+="<tr><th>Page<th>Views</tr>\n"
      for (page, times) in x:
         msg+="<tr><td>%s<td>%s</tr>\n" % (page, times)
      msg+="</table>\n"

      return(msg)

###############################################

if __name__ == "__main__":

# get parameters
    parser = OptionParser(usage=" %prog -r [--range] date")
    parser.add_option("-r", "--range", dest="range",
                      help="today - uses latest data\ndd/Mon/YYYY (e.g. 02/Jun/2015)\nall - all we've got for this month")
    (options, args) = parser.parse_args()

    if options.range:
        range=options.range
    else:
        range=None

    # handler for IP lookups
    h=IPLookup()

    # get data
    c=ApacheReader(h)
    c.loadfile(range)
    c.dostuff()


    # save what we know
    h.save()

    # run the report
    Report(c, range)



