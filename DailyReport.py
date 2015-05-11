#!/usr/bin/python

import smtplib, time, json
from insightly import Insightly
import datetime
import locale
import sys


# for development we use local data. Set dev to False to run in production or if you want to
# download a new version of the real data. Unless you have an smtp server running, setting
# dev to False will generate an error when it tries to email the results.
dev=True
#dev=False

# Test settings
to={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}
frm={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}

# Prod settings
#to={"name" : "Reports", "email" : "reports@17ways.com.au"}
#frm={"name" : "Daily CRM Report", "email" : "reports@17ways.com.au"}




class crmHelper():
   global dev

   global TIMEAMOUNT

   def __init__(self):
# link to the crm
      if not dev:
         self.crm = Insightly(apikey="1b59c7a6-98cc-4788-b4ae-d063453e04ab")
      self.taglist={}
      self.idlist={}
      self.complist={}
      self.comptaglist={}
      self.noteslist={}             # maps contact ids to time of contact
      self.notesbyidlist={}         # maps note ids to time of contact
      self.loadContacts()
      self.loadNotes()
      self.loadTasks()
      self.loadCompanies()
      self.loadUsers()
      self.loadOpportunities()

   def loadContacts(self):
# get contacts

      if dev:
# load from file for testing
         self.contacts=json.load(open("crmdump.txt"))
      else:
         self.contacts = self.crm.getContacts()
         json.dump(self.contacts, open("crmdump.txt", "w"))

# map names to ids
      for x in self.contacts:
         self.idlist[x["CONTACT_ID"]]="%s %s" % (x["FIRST_NAME"], x["LAST_NAME"])

# map names to tags
      for x in self.contacts:
         if x.has_key("TAGS"):
            tags=x["TAGS"]
            for t in tags:
               thistag=t["TAG_NAME"]
               if self.taglist.has_key(thistag):
                  self.taglist[thistag].append(x["CONTACT_ID"])
               else:
                  self.taglist[thistag]=[]
                  self.taglist[thistag].append(x["CONTACT_ID"])

   def loadTasks(self):
      if dev:
# load from file for testing
         self.tasks=json.load(open("crmtaskdump.txt"))
      else:
         self.tasks = self.crm.getTasks()
         json.dump(self.tasks, open("crmtaskdump.txt", "w"))


   def loadNotes(self):
# get all notes

      if dev:
# load from file for testing
         self.notes=json.load(open("crmnotedump.txt"))
      else:
         self.notes = self.crm.getNotes()
         json.dump(self.notes, open("crmnotedump.txt", "w"))

# check we have made notes recently
      for who in self.idlist.keys():                            # go through all contacts and work out last contact time
         for x in self.notes:
            for y in x['NOTELINKS']:                                                                   # go through all of the note links
               name=y['CONTACT_ID']                                                                  # get the associated contact
               if name==who:
                  time_added=datetime.datetime.strptime(x['DATE_UPDATED_UTC'], "%Y-%m-%d %H:%M:%S")   # update time
                  now=datetime.datetime.utcnow()
                  elapsed = now - time_added
                  if self.noteslist.has_key(who):
                     if self.noteslist[who]>elapsed.days:
                        self.noteslist[who]=elapsed.days
                  else:
                        self.noteslist[who]=elapsed.days

# get id of recent notes
      for x in self.notes:
         time_added=datetime.datetime.strptime(x['DATE_UPDATED_UTC'], "%Y-%m-%d %H:%M:%S")   # update time
         now=datetime.datetime.utcnow()
         elapsed = now - time_added
         if (elapsed.days * 60*60*24) + elapsed.seconds < TIMEAMOUNT:
            self.notesbyidlist[x['NOTE_ID']]=(elapsed.days * 60*60*24) + elapsed.seconds
         

   def loadCompanies(self):
# get companies

      if dev:
# load from file for testing
         self.companies=json.load(open("crmcompdump.txt"))
      else:
         self.companies = self.crm.getOrganizations()
         json.dump(self.companies, open("crmcompdump.txt", "w"))

# map names to ids
      for x in self.companies:
         self.complist[x["ORGANISATION_ID"]]=x["ORGANISATION_NAME"]

# map names to tags
      for x in self.companies:
         if x.has_key("TAGS"):
            tags=x["TAGS"]
            for t in tags:
               thistag=t["TAG_NAME"]
               if self.comptaglist.has_key(thistag):
                  self.comptaglist[thistag].append(x["ORGANISATION_ID"])
               else:
                  self.comptaglist[thistag]=[]
                  self.comptaglist[thistag].append(x["ORGANISATION_ID"])


   def loadUsers(self):
# get users

      if dev:
# load from file for testing
         self.users=json.load(open("crmuserdump.txt"))
      else:
         self.users = self.crm.getUsers()
         json.dump(self.users, open("crmuserdump.txt", "w"))

      self.username={}
      for x in self.users:
         self.username[x['USER_ID']] = x['FIRST_NAME']

   def getTag(self, tag):
      if self.taglist.has_key(tag):
         return(self.taglist[tag])
      else:
         print "Tag %s not found." % tag
         return([])

   def getEmpbyCompany(self):
      ret={}
      for x in self.contacts:
         comp=x['DEFAULT_LINKED_ORGANISATION']
         if comp<>None:
            if ret.has_key(comp):
               ret[comp]=ret[comp]+1
            else:
               ret[comp]=1

      tabsort=sorted(ret.items(), key=lambda x: x[1])
      tabsort.reverse()

      return(tabsort)

   def loadOpportunities(self):
      if dev:
# load from file for testing
         self.opportunities=json.load(open("crmoppsdump.txt"))
      else:
         self.opportunities = self.crm.getOpportunities()
         json.dump(self.opportunities, open("crmoppsdump.txt", "w"))

   def getOpportunities(self):
      ret=[]
      for x in self.opportunities:
         id=x['OPPORTUNITY_ID']
         name=x['OPPORTUNITY_NAME']
         amount=x['BID_AMOUNT']
         chance=x['PROBABILITY']

         owner=x['OWNER_USER_ID']
         details=x['OPPORTUNITY_DETAILS']

         if amount==None: amount=0
         if chance==None: chance=0
         if details==None: details=""

         ret.append({'id': id, 'name' : name, 'details' : details, 'amount' : amount, 'chance' : chance, 'owner' : self.username[owner]})
      return(ret)

   def getTag(self, tag):
      if self.taglist.has_key(tag):
         return(self.taglist[tag])
      else:
         print "Tag %s not found." % tag
         return([])

   def getTasks(self):
      ret=[]
      for x in self.tasks:
         id=x['TASK_ID']
         title=x['Title']
         d=x['DUE_DATE']
         t=datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")

         due=t.strftime('%d %b %Y')

# check if overdue
         now=datetime.datetime.now()
         if now>t:
            overdue=True
         else:
            overdue=False

         completed=x['COMPLETED']
         details=x['DETAILS']
         status=x['STATUS']
         who=self.username[x['RESPONSIBLE_USER_ID']]

         if not completed:
            ret.append({'id': id, 'overdue': overdue, 'title': title, 'due': due, 'completed': completed, 'details': details, 'status': status, 'who': who})
      return(ret)

   def getCompanyTag(self, tag):
      if self.comptaglist.has_key(tag):
         return(self.comptaglist[tag])
      else:
         print "Tag %s not found." % tag
         return([])

   def getAllTags(self):
      return(self.taglist.keys())

   def getAllCompanyTags(self):
      return(self.comptaglist.keys())

   def getNewContacts(self):
      newc=[]
      for x in self.contacts:
         time_added=datetime.datetime.strptime(x['DATE_CREATED_UTC'], "%Y-%m-%d %H:%M:%S")
         now=datetime.datetime.utcnow()
         elapsed = now - time_added
         if (elapsed.days * 60*60*24) + elapsed.seconds < TIMEAMOUNT:
            newc.append(x['CONTACT_ID'])
      return(newc)

   def getCompanieswithTag(self, tag):
      if self.comptaglist.has_key(tag):
          return(self.comptaglist[tag])
      else:
          return([])

   def getContactswithTag(self, tag):
      if self.taglist.has_key(tag):
          return(self.taglist[tag])
      else:
          return([])

   def getNewCompanies(self):
      newc=[]
      for x in self.companies:
         time_added=datetime.datetime.strptime(x['DATE_CREATED_UTC'], "%Y-%m-%d %H:%M:%S")
         now=datetime.datetime.utcnow()
         elapsed = now - time_added
         if (elapsed.days * 60*60*24) + elapsed.seconds < TIMEAMOUNT:
            newc.append(x['ORGANISATION_ID'])
      return(newc)

   def checkContact(self,who, days):
# check we have made notes recently - return True/False and number of days since contact
      if self.noteslist.has_key(who):
         if self.noteslist[who]<=days:
            return(True, self.noteslist[who])
         else:
            return(False, self.noteslist[who])
      else:
         return(False, None)


   def getTagwithNoContact(self, tag, days):
# return list of contacts with no comms
      ret=[]
      for p in self.taglist[tag]:
         (flag, d) = self.checkContact(p, days)
         if not flag:
            ret.append([p, d])
      return(ret)

   def getNote(self, id):
      for x in self.notes:
         if x['NOTE_ID']==id:
            return(x)

   def getNewNotes(self):
      data=[]
      tabsort=sorted(self.notesbyidlist.items(), key=lambda x: x[1])
#      tabsort.reverse()
      for x in tabsort:
         noteid=x[0]
         n=self.getNote(noteid)
         who=self.username[n['OWNER_USER_ID']]
         con=""
         for y in n['NOTELINKS']:
            name=y['CONTACT_ID']
            if name<>None:
               con+=self.idlist[name]
         title=n['TITLE']
         body=n['BODY']
         data.append([who, con, title, body])
      return(data)

##############################################
#                                            #
#                                            #
#            Generate the report             #
#                                            #
#                                            #
##############################################
class Report():

   global TIMEWORDS, TIMEAMOUNT

   global frm, to

   def __init__(self, c):
      self.c=c
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
      self.message+="<td valign=middle><font size=96 color='#5d73b6'>CRM Daily Report - %s</font></tr></table><hr>" % day
      self.message+="Overview of how we are tracking in our contact with customers. The report is only as good as the data, so sort yourselves out, you fuckers."

   def run(self):
# This is the orchestrator function. Change this to change the order of the sections etc.
      self.newContacts()
      self.newCompanies()
      self.recentNotes()
      self.checkNotes()
      self.Opportunities()
      self.activeCompanies()
      self.activeContacts()
      self.openTasks()
      self.detailsbreak()
      self.linkedInbyPerson()
      self.Opportunities(details=True)
      self.byTag()
      self.byCompanyTag()
      self.byCompanyBreakdown()
      self.byLocation()
      self.finish()

   def Opportunities(self, details=None):
      self.message+="<hr><h2>Opportunities"
      if details: self.message+=" in Detail"
      self.message+="</h2>"

      self.message+="<h4>Show what we have going on.</h4>"
      data=self.c.getOpportunities()

# charts only for the detail part

      if details:

          titlist   =[]
          chancelist=[]
          amountlist=[]

          for x in data:
             titlist.append(x['name'])
             chancelist.append(x['chance'])
             amountlist.append(x['amount'])

    # scale the numbers or the charts are fucked
          topamt=max(amountlist)

    # charts

    # chart by total amount

          self.message+="<h3>By Total Amount</h3>"

          databit="chd=t:"
          titbit="chdl="
          for i in range(0,len(titlist)-1):
             databit+=str(amountlist[i]/(topamt/100)) + ","
             titbit+=titlist[i] + "|"

    # strip last comma or bar
          databit=databit[:-1]
          titbit=titbit[:-1]

    # replace spaces
          titbit=titbit.replace(" ","%20")

          url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&chco=FFC6A5|FFFF42|DEF3BD|00A5C6|DEBDDE&" + databit + "&" + titbit

          self.message+="<img height=300 width=580 src='%s'>" % url

    # chart by total ratio

          self.message+="<h3>By Relative Value</h3>"

          databit="chd=t:"
          titbit="chdl="
          for i in range(0,len(titlist)-1):
             databit+=str(amountlist[i]/(topamt/100) * chancelist[i]) + ","
             titbit+=titlist[i] + "|"

    # strip last comma or bar
          databit=databit[:-1]
          titbit=titbit[:-1]

    # replace spaces
          titbit=titbit.replace(" ","%20")

          url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&chco=FFC6A5|FFFF42|DEF3BD|00A5C6|DEBDDE&" + databit + "&" + titbit

          self.message+="<img height=300 width=580 src='%s'>" % url

   # print out tables with summary

      if details:
# use locale to add commas to numbers, python 2.6 doesn't have format
          locale.setlocale(locale.LC_ALL, '')

          self.message+= "<table class='nice' border=1><tr><th>Opportunity<th>Potential Profit<th>Probability<th>Ratio</tr>"
          for x in data:
             try:
                num=locale.format("%d", int(x['amount']), grouping=True)
                ratio=locale.format("%d", int(x['amount'] / 100 / x['chance']), grouping=True)
             except:
                num="Unknown"
                ratio = "Huge"
             self.message+="<tr><td style='text-align: left;'>%s<td>$%s<td>%s<td>%s</tr>" % (x['name'],num,x['chance'],ratio)

          self.message+="</table>"


      for x in data:
         if details:
            self.message+="<h3><a href=https://y31b3txz.insight.ly/opportunities/details/%s>%s</a> - Owner: %s</h3>" % (x['id'],x['name'],x['owner'])
            try:
                num=locale.format("%d", int(x['amount']), grouping=True)
            except:
               num="Unknown"
            self.message+="<b>Value:</b>$%s<br>" % num
            self.message+="<b>Chance:</b>%s%%<br><br>" % x['chance']
            self.message+=x['details']
         else:
            self.message+="<a href=https://y31b3txz.insight.ly/opportunities/details/%s>%s</a> - Owner: %s<br>" % (x['id'],x['name'],x['owner'])

   def openTasks(self):
      self.message+="<hr><h2>Open Tasks</h2>"

      self.message+="<i>Tasks we have allocated to ourselves to do.</i>"

      data=self.c.getTasks()
      if len(data)>0:
          self.message+="<table class='nice' border=1>"
          self.message+="<tr><th>What<th>Who<th>When<th>Status</tr>"
          for x in data:
             if x['overdue']:
                x['due']="<td style='color:red; font-weight: bold;'>%s" % x['due']
             else:
                x['due']="<td>%s" % x['due']
             self.message+="<tr><td><a href='https://y31b3txz.insight.ly/Tasks/TaskDetails/%s' title='%s'>%s</a><td>%s%s<td>%s</th>" % (x['id'],x['details'],x['title'],x['who'],x['due'],x['status'])
          self.message+="</table>"


   def linkedInbyPerson(self):
      self.message+="<hr><h2>LinkedIn Data in the CRM</h2>"

      self.message+="<i>Who is connected with a customer on LinkedIn and how much overlap is there.</i>"

      # overview of list - get all of our contacts
      john=self.c.getTag("LIContact-John")
      mark=self.c.getTag("LIContact-Mark")
      tim=self.c.getTag("LIContact-Tim")

      j=len(john) / 10
      m=len(mark) / 10
      t=len(tim) / 10
      # get the intersections - divide by 10 so they look ok
      jt=len( list(set(john) & set(tim)) ) / 10
      jm=len( list(set(john) & set(mark)) ) / 10
      mt=len( list(set(mark) & set(tim)) ) / 10
      jtm=len( list(set(mark) & set(tim) & set(john)) ) / 10

      url="https://chart.googleapis.com/chart?cht=v&chs=580x300&chd=t:%s,%s,%s,%s,%s,%s,%s&chco=FF6342,ADDE63,63C6DE&chdl=John%%20Tufts%%20(%s)|Mark%%20Guthrie%%20(%s)|Tim%%20Mallyon(%s)" \
          % (j,m,t,jm,jt,mt,jtm,len(john),len(mark),len(tim))

      self.message+="<img height=300 width=580 src='%s'>" % url

      # compare LinkedIn to other data
      self.message+="<hr><h2>LinkedIn vs Directly Entered</h2>"
      self.message+="<h4>Where are our contacts coming from?</h4>"

      lin=len( list(set(mark) | set(tim) | set(john)) )

      url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&chd=t:%s,%s&chco=FF6342,ADDE63,63C6DE&chdl=LinkedIn(%s)|Other(%s)" \
          % (lin, len(self.c.contacts) - lin,lin, len(self.c.contacts) - lin)

      self.message+="<img height=300 width=580 src='%s'>" % url

   def detailsbreak(self):
      self.message+="<hr><hr><h1>Details Below...</h1><img src='http://17ways.com.au/english_gent.jpg'><h1>Read on old chap, read on....</h1><hr>"
      

   def byTag(self):
# breakdown by tags

      self.message+="<hr><h2>Breakdown of Tags on Contacts</h2>"
      self.message+="<h4>Numbers of people by tag type.</h4>"

# Skills

      tab={}

      for x in self.c.getAllTags():
         if x.find("Skill-")==0:   # only get skills
            y=x.replace("Skill-","")
            tab[y]=len(self.c.getTag(x))   # get how many have this tag

      tabsort=sorted(tab.items(), key=lambda x: x[1])

      tabsort.reverse()

# create the url for the chart
      part="chd=t:"
      for x in tabsort:
         part+="%s," % x[1]
      part=part[:-1]
      part+="&chdl="
      for x in tabsort:
         part+="%s," % x[0]
      part=part[:-1]

      part=part.replace(" ","%20")

      url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&" + part

      self.message+="<img height=300 width=580 src='%s'>" % url

      self.message+="<br><br><table  class='nice' border=1>"
      self.message+="<tr><th>Skill<th>Number of Entries</tr>"


      for x in tabsort:
         self.message+="<tr><td><a href='https://y31b3txz.insight.ly/contacts/tags/?t=Skill-%s'>%s</a><td>%s</tr>" % (x[0], x[0], x[1])

      self.message+="</table>"

# Type

      tab={}

      for x in self.c.getAllTags():
         if x.find("Type-")==0:   # only get skills
            y=x.replace("Type-","")
            tab[y]=len(self.c.getTag(x))   # get how many have this tag

      tabsort=sorted(tab.items(), key=lambda x: x[1])

      tabsort.reverse()

# create the url for the chart
      part="chd=t:"
      for x in tabsort:
         part+="%s," % x[1]
      part=part[:-1]
      part+="&chdl="
      for x in tabsort:
         part+="%s," % x[0]
      part=part[:-1]

      part=part.replace(" ","%20")

      url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&" + part

      self.message+="<img height=300 width=580 src='%s'>" % url

      self.message+="<br><br><table  class='nice' border=1>"
      self.message+="<tr><th>Type<th>Number of Entries</tr>"


      for x in tabsort:
         self.message+="<tr><td><a href='https://y31b3txz.insight.ly/contacts/tags/?t=Type-%s'>%s</a><td>%s</tr>" % (x[0], x[0], x[1])

      self.message+="</table>"


   def byCompanyTag(self):
# breakdown by tags

         self.message+="<hr><h2>Breakdown of Tags on Organisations</h2>"
         self.message+="<h4>Numbers of organisations by tag type.</h4>"

         tab={}

         for x in self.c.getAllCompanyTags():
            tab[x]=len(self.c.getCompanyTag(x))   # get how many have this tag

         tabsort=sorted(tab.items(), key=lambda x: x[1])

         tabsort.reverse()

# create the url for the chart
         part="chd=t:"
         for x in tabsort:
            part+="%s," % x[1]
         part=part[:-1]
         part+="&chdl="
         for x in tabsort:
            part+="%s," % x[0]
         part=part[:-1]

         part=part.replace(" ","%20")

         url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&" + part

         self.message+="<img height=300 width=580 src='%s'>" % url

         self.message+="<br><br><table  class='nice' border=1>"

         self.message+="<tr><th>Tag Name<th>Number of Matches</tr>"

         for x in tabsort:
            self.message+="<tr><td><a href='https://y31b3txz.insight.ly/contacts/tags/?t=%s'>%s</a><td>%s</tr>" % (x[0], x[0], x[1])

         self.message+="</table>"

   def activeCompanies(self):
# list companies marked as active
      self.message+="<hr><h2>Active Companies</h2>"
      self.message+="<h4>These are the companies we are actively pursing opportunities with.</h4>"

      list=self.c.getCompanieswithTag("Company-Active")

      for x in list:
         self.message+="<a href='https://y31b3txz.insight.ly/organisations/Details/%s'>%s</a><br>" % (x, self.c.complist[x])


   def activeContacts(self):
# list contacts marked as active
      self.message+="<hr><h2>Active Contacts</h2>"
      self.message+="<h4>These are the contacts we are actively pursing opportunities with.</h4>"

      list=self.c.getContactswithTag("Type-Active")

      for x in list:
         self.message+="<a href='https://y31b3txz.insight.ly/organisations/Details/%s'>%s</a><br>" % (x, self.c.idlist[x])

   def byLocation(self):
# breakdown by location tags
         f=open("countries.txt")
         countries={}
         for line in f.readlines():
            x=line.split(",")
            code=x[1].strip()
            where=x[0]
            countries[code]=where

         self.message+="<hr><h2>Breakdown by Location</h2>"
         self.message+="<h4>Numbers of people by where they are based. Graph excludes Australia.</h4>"

         tab={}

         for x in self.c.getAllTags():
            if x.find("Location")==0:
               tab[x]=len(self.c.getTag(x))   # get how many have this tag

         tabsort=sorted(tab.items(), key=lambda x: x[1])

         tabsort.reverse()

         # create the url for the chart - bar chart ex. Aus.

         # take a copy of the data and summarise it a bit
         tabsortchart=tabsort[1:8]   # first few minus Australia
         therest=tabsort[9:]
         others=0
         for i in therest:
            others+=i[1]
         tabsortchart.append(['Others',others])


         part="chd=t:"
         for x in tabsortchart[1:]:
            part+="%s," % x[1]
         part=part[:-1]
         part+="&chdl="
         for x in tabsortchart[:8]:
            lo=x[0].replace("Location-","")
            part+="%s|" % lo
         part=part[:-1]

         part=part.replace(" ","%20")

         url="https://chart.googleapis.com/chart?cht=bvg&chs=580x300&chco=000000|FF0000|00FF00|0000FF&" + part
         self.message+="<br><br><img height=300 width=580 src='%s'>" % url

          # create the url for the chart - Aus vs Rest of World. Cricket.

          # take a copy of the data and summarise it a bit
          # google charts are shit, so scale the numbers down
         high=tabsort[0][1]   # count in Oz
         scale=10 ** (len(str(high)) -2)   # reduce it to less than 100 or the graphs are fucked

         others=0
         for i in tabsort[1:]:
            others+=i[1]
         tabsortchart=[tabsort[0]]
         tabsortchart.append(['Rest of World',others])

         part="chd=t:"
         for x in tabsortchart:
            part+="%s," % (int(x[1]) / scale)
         part=part[:-1]
         part+="&chdl="
         for x in tabsortchart[:8]:
            lo=x[0].replace("Location-","")
            part+="%s|" % lo
         part=part[:-1]
         part=part.replace(" ","%20")

         url="https://chart.googleapis.com/chart?cht=p3&chs=400x400&chco=FF0000|0000FF&" + part
         self.message+="<br><br><img height=400 width=400 src='%s'>" % url

         self.message+="<br><br><table  class='nice' border=1>"
         self.message+="<tr><th>Country<th>Number of Contacts</tr>"

         for x in tabsort:
            code=x[0].replace("Location-","")
            try:
               where=countries[code]
            except:
               where="Unknown"
            self.message+="<tr><td><a href='https://y31b3txz.insight.ly/contacts/tags/?t=%s'>%s</a><td>%s</tr>" % (x[0], where, x[1])

         self.message+="</table>"



   def newContacts(self):
# New contacts
      newbies = self.c.getNewContacts()

      if len(newbies)>0:
         self.message+="<hr><h2>New Contacts</h2>"
         self.message+="<h4>New contacts added %s.</h4>" % TIMEWORDS

         for x in newbies:
            self.message+="<a href='https://y31b3txz.insight.ly/Contacts/Details/%s'>%s</a><br>" % (x, self.c.idlist[x])

   def newCompanies(self):
# New companies
      newbies = self.c.getNewCompanies()

      if len(newbies)>0:
         self.message+="<hr><h2>New Organisations</h2>"
         self.message+="<h4>New companies added %s.</h4>" % TIMEWORDS

         for x in newbies:
            self.message+="<a href='https://y31b3txz.insight.ly/organisations/Details/%s'>%s</a><br>" % (x, self.c.complist[x])


   def checkNotes(self):
      # Tagged people with no contact
      # format of list is Tag-name : [days to check, "Title for message"
         imp={"Type-DM" : [30, "Decision Makers", "People we consider important and who could open doors for us. So why aren't we calling them?"],   \
              "Type-Active" : [30, "Active", "People we are actively pursuing something with, but can't be arsed to talk to. Or maybe we don't love the CRM and just haven't been updating it. Well let me tell you, you need to love the CRM."]}

         for x in imp.keys():
            data=self.c.getTagwithNoContact(x, imp[x][0])
            if len(data)==0:
               self.message+="<hr><h2>%s - All Uptodate!</h2>" % imp[x][1]
            else:
               self.message+="<hr><h2>%s - Overdue Contact</h2>" % imp[x][1]
               self.message+="<h4>%s</h4>" % imp[x][2]
               for y in data:
                  self.message+="<a href='https://y31b3txz.insight.ly/Contacts/Details/%s'>%s</a>" % (y[0], self.c.idlist[y[0]])
                  if y[1]==None:
                     self.message+=" - no contact ever.<br>"
                  else:
                     self.message+=" - no contact for %s days.<br>" % y[1]

   def recentNotes(self):
      self.message+="<hr><h2>New Notes</h2>"
      self.message+="<h4>New notes added %s.</h4>" % TIMEWORDS
      data=self.c.getNewNotes()
      for x in data:
         self.message+="<h3>%s with %s: %s</h3>%s" % (x[0], x[1], x[2], x[3])

   def byCompanyBreakdown(self):
      self.message+="<hr><h2>Breakdown by Company</h2>"
      self.message+="<h4>Shows where our contacts work.</h4>"
      data=self.c.getEmpbyCompany()
      self.message+="<table class='nice' border=1>"
      self.message+="<tr><th>Company<th>Number of Contacts</tr>"

      for x in data:
         self.message+="<tr><td style='text-align: left;'>%s<td>%s</tr>" % (self.c.complist[x[0]], x[1])

      self.message+="</table>"

   def finish(self):
# Footer for the email
      self.message+="</body></html>"

      self.message=self.message.encode('ascii', 'ignore').decode('ascii')

      if dev:
         f=open("temp.html", "w")
         for line in self.message:
            f.write(line)
         f.close()
      else:
         
         smtpObj = smtplib.SMTP('localhost')
         smtpObj.sendmail(frm['email'], [to['email']], self.message)

# don't check these, because I can't be bothered.

# Call with words to put in the description and number of seconds to check backwards for.

if len(sys.argv)>1:
   TIMEWORDS=sys.argv[1]
   TIMEAMOUNT=int(sys.argv[2])
else:
   TIMEWORDS=" in the last 24 hours"
   TIMEAMOUNT=60 * 60 * 25


# load the helper class for CRM
c=crmHelper()

# run the report
Report(c).run()



