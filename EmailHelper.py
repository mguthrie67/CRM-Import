#!/usr/bin/python

# Helper function to send emails to us
#
# Use:
#
# import EmailHelper
# EmailHelper.send("Title", "<h1>Hello</h1>This is an email.")

import smtplib, time, json
import datetime
import locale
import sys


# Test settings
to={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}
frm={"name" : "Mark Guthrie", "email" : "mark.guthrie@17ways.com.au"}

# Prod settings
#to={"name" : "Reports", "email" : "reports@17ways.com.au"}
#frm={"name" : "Daily CRM Report", "email" : "reports@17ways.com.au"}

class send():

   global frm, to

   def __init__(self, title, msg):
      self.message=""

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

""" % (frm["name"], frm["email"], to["name"], to["email"], title)

      self.message+="<table width=100%%><tr><td><img width=120px src=http://17ways.com.au/images/logo_slogan.png>"
      self.message+="<td valign=middle><font size=96 color='#5d73b6'>%s</font></tr></table><hr>" % title
      self.message+=msg

      self.message+="</body></html>"

      self.message=self.message.encode('ascii', 'ignore').decode('ascii')

         
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(frm['email'], [to['email']], self.message)

