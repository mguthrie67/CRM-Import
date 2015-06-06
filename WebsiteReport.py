#!/usr/bin/python

import gzip
import time
import shlex
#from urllib2 import urlopen
#from contextlib import closing
import urllib
import json
import socket
import smtplib

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
        self.us="122.109.192.180"

# counters

        self.spiderscnt=0
        self.uscnt=0
        self.noisecnt=0

# big list

        self.visitors=[]

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
    # check for us
                url=request.split()[1]
                url=url.replace("%20"," ")
                if url=="/" : url="the homepage"

                stuff=self.IPHandler.getLocation(ip)

    # add our other stuff
                stuff["url"]=url
                stuff["ip"]=ip
                stuff["request"]=request
                stuff["rc"]=rc
                stuff["referrer"]=referrer
                stuff["agent"]=agent

                if ip==self.us:
                    stuff["us"]=True
                else:
                    stuff["us"]=False

#                print stuff

                self.visitors.append(stuff)

#                if ip==self.us:
#                    print "You clowns. Looking at %s." % url
#                else:
#                    print "%s in %s. Looking at %s." % (loc["city"], loc["country_name"], url)
#                    print "########################################################"
#                    print "    IP   : %s" % ip
#                    print "    Agent: %s" % agent
#                    print "########################################################"


    def printit(self):

        txt=""

        for x in self.visitors:
            txt+=x['ip'] + "<br>"

        return(txt)

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

      self.message+=self.data.printit()

      f=open("WebDaily.html", "w")
      for line in self.message:
         f.write(line)
      f.close()

#      smtpObj = smtplib.SMTP('localhost')
#      smtpObj.sendmail(frm['email'], [to['email']], self.message)

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



