#!/usr/bin/python

import smtplib, time, json
from insightly import Insightly
import datetime

dev=True
#dev=False

to={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}
frm={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}

class crmHelper():
   global dev

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
         if (elapsed.days * 60*60*24) + elapsed.seconds < 60*60*25:
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
         ret.append({'id': id, 'name' : name, 'details' : details, 'amount' : amount, 'chance' : chance, 'owner' : self.username[owner]})
      return(ret)

   def getTag(self, tag):
      if self.taglist.has_key(tag):
         return(self.taglist[tag])
      else:
         print "Tag %s not found." % tag
         return([])
      

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
         if (elapsed.days * 60*60*24) + elapsed.seconds < 60*60*25:
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
         if (elapsed.days * 60*60*24) + elapsed.seconds < 60*60*25:
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
# Generate the report                        #
##############################################
class Report():

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
	font-size: 400%%;
}

h2 {
	font-size: 140%%;
}
</style>
</head>
<body>

""" % (frm["name"], frm["email"], to["name"], to["email"], "Daily Report - " + day)

      self.message+="<table width=100%%><tr><td><img width=120px src=http://17ways.com.au/images/logo_slogan.png>"
      self.message+="<td valign=middle><font size=96>CRM Daily Report - %s</font></tr></table><hr>" % day
      self.message+="Overview of how we are tracking in our contact with customers."

   def run(self):
# This is the orchestrator function. Change this to change the order of the sections etc.
      self.newContacts()
      self.newCompanies()
      self.recentNotes()
      self.checkNotes()
      self.Opportunities()
      self.activeCompanies()
      self.activeContacts()
      self.detailsbreak()
      self.linkedInbyPerson()
      self.Opportunities(details=True)
      self.byTag()
      self.byCompanyTag()
      self.byLocation()
      self.finish()

   def Opportunities(self, details=None):
      self.message+="<hr><h2>Opportunities"
      if details: self.message+=" in Detail"
      self.message+="</h2>"

      self.message+="<i>Show what we have going on.</i><br>"
      data=self.c.getOpportunities()
      for x in data:
         if details:
            self.message+="<h3><a href=https://y31b3txz.insight.ly/opportunities/details/%s>%s</a> - Owner: %s</h3>" % (x['id'],x['name'],x['owner'])
            try:
               num="{:,}".format(int(x['amount']))
            except:
               num="Unknown"
            self.message+="<b>Value:</b>$%s<br>" % num
            self.message+="<b>Chance:</b>%s%%<br><br>" % x['chance']
            self.message+=x['details']
         else:
            self.message+="<br><a href=https://y31b3txz.insight.ly/opportunities/details/%s>%s</a> - Owner: %s" % (x['id'],x['name'],x['owner'])


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
      self.message+="<i>Where are our contacts coming from?</i>"

      lin=len( list(set(mark) | set(tim) | set(john)) )

      url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&chd=t:%s,%s&chco=FF6342,ADDE63,63C6DE&chdl=LinkedIn(%s)|Other(%s)" \
          % (lin, len(self.c.contacts) - lin,lin, len(self.c.contacts) - lin)

      self.message+="<img height=300 width=580 src='%s'>" % url

   def detailsbreak(self):
      self.message+="<hr><hr><h1>Details Below</h1><hr>"
      

   def byTag(self):
# breakdown by tags

      self.message+="<hr><h2>Breakdown of Tags on Contacts</h2>"
      self.message+="<i>Numbers of people by tag type.</i><br><br>"

      tab={}

      for x in self.c.getAllTags():
         if x.find("Location")<>0 and x.find("LIContact")<>0:   # ignore the locations and contacts
            tab[x]=len(self.c.getTag(x))   # get how many have this tag

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

      self.message+="<br><br><table border=1>"

      for x in tabsort:
         self.message+="<tr><td><a href='https://y31b3txz.insight.ly/contacts/tags/?t=%s'>%s</a><td>%s</tr>" % (x[0], x[0], x[1])

      self.message+="</table>"

   def byCompanyTag(self):
# breakdown by tags

         self.message+="<hr><h2>Breakdown of Tags on Organisations</h2>"
         self.message+="<i>Numbers of organisations by tag type.</i><br><br>"

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

         self.message+="<br><br><table border=1>"

         for x in tabsort:
            self.message+="<tr><td><a href='https://y31b3txz.insight.ly/contacts/tags/?t=%s'>%s</a><td>%s</tr>" % (x[0], x[0], x[1])

         self.message+="</table>"

   def activeCompanies(self):
# list companies marked as active
      self.message+="<hr><h2>Active Companies</h2>"
      self.message+="<i>These are the companies we are actively pursing opportunities with.</i><br><br>"

      list=self.c.getCompanieswithTag("Company-Active")

      for x in list:
         self.message+="<a href='https://y31b3txz.insight.ly/organisations/Details/%s'>%s</a><br>" % (x, self.c.complist[x])


   def activeContacts(self):
# list contacts marked as active
      self.message+="<hr><h2>Active Contacts</h2>"
      self.message+="<i>These are the contacts we are actively pursing opportunities with.</i><br><br>"

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
         self.message+="<i>Numbers of people by where they are based.</i>"

         tab={}

         for x in self.c.getAllTags():
            if x.find("Location")==0:
               tab[x]=len(self.c.getTag(x))   # get how many have this tag

         tabsort=sorted(tab.items(), key=lambda x: x[1])

         tabsort.reverse()

         # create the url for the chart
         part="chd=t:"
         for x in tabsort[:8]:
            part+="%s," % x[1]
         part=part[:-1]
         part+="&chdl="
         for x in tabsort[:8]:
            lo=x[0].replace("Location-","")
            part+="%s|" % lo
         part=part[:-1]

         part=part.replace(" ","%20")

         url="https://chart.googleapis.com/chart?cht=bvg&chs=580x300&chco=00000,FF0000|00FF00|0000FF&" + part
         self.message+="<br><br><img height=300 width=580 src='%s'>" % url

         self.message+="<br><br><table border=1>"

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
         self.message+="<i>New contacts added in the last 24 hours.</i><br>"

         for x in newbies:
            self.message+="<br><a href='https://y31b3txz.insight.ly/Contacts/Details/%s'>%s</a>" % (x, self.c.idlist[x])

   def newCompanies(self):
# New companies
      newbies = self.c.getNewCompanies()

      if len(newbies)>0:
         self.message+="<hr><h2>New Organisations</h2>"
         self.message+="<i>New companies added in the last 24 hours.</i><br>"

         for x in newbies:
            self.message+="<br><a href='https://y31b3txz.insight.ly/organisations/Details/%s'>%s</a>" % (x, self.c.complist[x])


   def checkNotes(self):
      # Tagged people with no contact
      # format of list is Tag-name : [days to check, "Title for message"
         imp={"Type-DM" : [30, "Decision Makers"],   \
              "Type-Active" : [30, "Active"]}

         for x in imp.keys():
            data=self.c.getTagwithNoContact(x, imp[x][0])
            if len(data)==0:
               self.message+="<hr><h2>%s - All Uptodate!</h2>" % imp[x][1]
            else:
               self.message+="<hr><h2>%s - Overdue Contact</h2>" % imp[x][1]
               for y in data:
                  self.message+="%s" % self.c.idlist[y[0]]
                  if y[1]==None:
                     self.message+=" - no contact ever.<br>"
                  else:
                     self.message+=" - no contact for %s days.<br>" % y[1]

   def recentNotes(self):
      self.message+="<hr><h2>New Notes</h2>"
      self.message+="<i>New notes added in the last 24 hours.</i><br>"
      data=self.c.getNewNotes()
      for x in data:
         self.message+="<h3>%s with %s: %s</h3>%s" % (x[0], x[1], x[2], x[3])

   def finish(self):
# Footer for the email
      self.message+="</body></html>"

      if dev:
         f=open("temp.html", "w")
         for line in self.message:
            f.write(line)
         f.close()
      else:
         
         smtpObj = smtplib.SMTP('localhost')
         smtpObj.sendmail(frm['email'], [to['email']], self.message)         

# load the helper class for CRM
c=crmHelper()

# run the report
Report(c).run()



