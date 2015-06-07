#!/usr/bin/python

##### TODO
###
### Have a web page to hold details
### Option on webpage to add to spiders
### Read spiders from a file
### Change to be __main__
### Weekly option to slowly rebuild known IP info
### Fix format on when
### remove request specific fields from visitors
### Add list of requests to visitorsdetails
### Add popular pages list

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
        self.visitorcount={}        # mapping of IP to pages visited
        self.pagesvisited={}        # mapping of page name to IP addresses that visited it
        self.newvisitor=[]          # visits from people we haven't seen before
        self.countries={}           # mapping of country codes to a list of IPs from there

###########################
# load the file           #
###########################
    def loadfile(self):

# open the file

        self.filehandle=gzip.open("17ways.com.au-Jun-2015.gz")


############################
# return next line of file #
############################
    def getnext(self):

        return(self.filehandle.readline())


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

####
# Number of visits
####
            if self.visitorcount.has_key(x['ip']):
                self.visitorcount[x['ip']]=self.visitorcount[x['ip']]+1
            else:
                self.visitorcount[x['ip']]=1




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
                url=request.split()[1]
                url=url.replace("%20"," ")
                if url=="/" : url="the homepage"

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

     #   print self.visitors['37.187.142.28']
     #   print self.visitors['66.249.75.85']

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

   def __init__(self, c):
      self.data=c
      self.message=""
# Basic heading stuff for the email.
      day=time.strftime("%A")

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

""" % (frm["name"], frm["email"], to["name"], to["email"], "Daily Report - " + day)

      self.message+="<table width=100%%><tr><td><img width=120px src=http://17ways.com.au/images/logo_slogan.png>"
      self.message+="<td valign=middle><font size=96 color='#5d73b6'>Website Report - %s</font></tr></table><hr>" % day
      self.message+="Who has been on our website in the last 24 hours.<br>"

      self.message+=self.printVisitors()
      self.message+=self.printVisitorsDetails()

      f=open("WebDaily.html", "w")
      for line in self.message:
         f.write(line)
      f.close()

#      smtpObj = smtplib.SMTP('localhost')
#      smtpObj.sendmail(frm['email'], [to['email']], self.message)

   def printVisitors(self):
      x=self.data.dataTotalVisitors()
      msg="<h2>Top Visitors</h2>\n"
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
          msg+="\n\n<h3 id='%s'>%s</h3><table class='nice' border=1 width='80%%'>\n" % (ip, ip)
          msg+="<tr><th width='30%'>Attribute<th width='70%'>Value</tr>\n"
          y=self.data.visitors[ip]
          for k in y.keys():
             msg+="<tr><td width='30%%'>%s<td width='70%%'>%s</tr>\n" % (k, y[k])
      msg+="</table>\n\n"

      return(msg)



# handler for IP lookups
h=IPLookup()

# get data
c=ApacheReader(h)
c.loadfile()
c.dostuff()


# save what we know
h.save()

# run the report
Report(c)



