#!/usr/bin/python

import smtplib, time, json
from insightly import Insightly
from HTMLEmailHelper import HTMLEmailHelper

dev=True
#dev=False

to={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}
frm={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}

class crmHelper():
   global dev

   def __init__(self):
# link to the crm
      self.crm = Insightly(apikey="1b59c7a6-98cc-4788-b4ae-d063453e04ab")
      self.taglist={}
      self.idlist={}

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

   def getTag(self, tag):
      if self.taglist.has_key(tag):
         return(self.taglist[tag])
      else:
         print "Tag %s not found." % tag
         return([])

   def getAllTags(self):
      return(self.taglist.keys())

##############################################
# Run through generating the report in order #
##############################################

# load the helper class for CRM
c=crmHelper()
c.loadContacts()

# load the helper class for email
h=HTMLEmailHelper(frm, to)

# headings
day=time.strftime("%A")
message=h.header("Daily Report - " + day)
message+="<br>"
message+=h.img2("http://17ways.com.au/images/logo_slogan.png")
message+="<br>"
message+=h.h1("CRM Daily Report - " + day)
message+="Overview of how we are tracking in our contact with customers."

message+=h.h2("LinkedIn Data in the CRM")

message+=h.i("Who is connected with a customer on LinkedIn and how much overlap is there.")

# overview of list - get all of our contacts
john=c.getTag("LIContact-John")
mark=c.getTag("LIContact-Mark")
tim=c.getTag("LIContact-Tim")

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

message+=h.img1(url)

# compare LinkedIn to other data
message+=h.h2("LinkedIn vs Directly Entered")
message+=h.i("Where are our contacts coming from?")

lin=len( list(set(mark) | set(tim) | set(john)) )

url="https://chart.googleapis.com/chart?cht=p3&chs=580x300&chd=t:%s,%s&chco=FF6342,ADDE63,63C6DE&chdl=LinkedIn(%s)|Other(%s)" \
    % (lin, len(c.contacts) - lin,lin, len(c.contacts) - lin)

message+=h.img1(url)

# breakdown by tags

message+=h.h2("Breakdown of Tags")
message+=h.i("Numbers of people by tag type.")

message+="<table class='button' border=1>"

tab={}

for x in c.getAllTags():
   if x.find("Location")<>0 and x.find("LIContact")<>0:   # ignore the locations
      tab[x]=len(c.getTag(x))   # get how many have this tag

tabsort=sorted(tab.items(), key=lambda x: x[1])

tabsort.reverse()

for x in tabsort:
   message+="<tr><td>%s<td>%s</tr>" % (x[0], x[1])

message+=h.footer()

if dev:
   f=open("temp.html", "w")
   for line in message:
      f.write(line)
   f.close()
else:
   try:
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(frm['email'], [to['email']], message)         
   except SMTPException:
      print "Error: unable to send email"