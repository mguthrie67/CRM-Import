#!/bin/env python
# pip install insightly-python
# pip install python-linkedin

################################################################################
# Classes to handle getting data from LinkedIn and importing it to the CRM.    #
# class crm handles all of the interaction with Insightly.                     #
# class linkedIn handles the linkedIn stuff.                                   #
# class controller manages the logic and flows between them.                   #
#                                                                              #
# You can import these do work directly with the systems or just run it and it #
# will go through and apply any updates to Insighly from linkedIn.             #
################################################################################

import json
from linkedin import linkedin
from insightly import Insightly

import base64
import urllib2
import sys

# Utility function to call the REST API for things that don't have a python API

def callREST(method, url, data):
    response = None
    text = ''
    baseurl = 'https://api.insight.ly'
    full_url = baseurl + url
    apikey="1b59c7a6-98cc-4788-b4ae-d063453e04ab"
            
    request = urllib2.Request(full_url)
    base64string = base64.encodestring('%s:%s' % (apikey, '')).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    request.get_method = lambda: method

    if method == 'PUT' or method == 'POST':
        request.add_header('Content-Type', 'application/json')
        result = urllib2.urlopen(request, data)
    else:
        result = urllib2.urlopen(request)
        text = result.read()


class crm():
################################
# data and methods for the crm #
################################

    def __init__(self, insight_key):
        
# link to the crm
        self.crm = Insightly(apikey=insight_key)

# load all contacts and orgs from crm
        self.load_insightly_contacts()
        self.load_insightly_orgs()

    def load_insightly_contacts(self):

# load contact ids from insightly #
        self.ins_contacts = {}
        conns = self.crm.getContacts()
        for c in conns:
            self.ins_contacts["%s %s" % (c['FIRST_NAME'],c['LAST_NAME'])] = c['CONTACT_ID']

    def addContact(self,dets,who):

# add a new contact, also a new org if required
        c={}
        c['CONTACT_ID']=0            # id=0 means add a new one
        c['FIRST_NAME']=dets["first-name"]
        c['LAST_NAME']=dets["last-name"]
        c['BACKGROUND']=dets["summary"]

# Tags for location and who owns the contact in Linked-In
        c['TAGS']=[]
        if dets["location-country"]<>None:
            c['TAGS'].append({"TAG_NAME" : "Location-%s" % dets["location-country"].upper()})
        c['TAGS'].append({"TAG_NAME" : "LIContact-%s" % who})

# linkedIn URL

        c["CONTACTINFOS"]=[{"SUBTYPE": "LinkedInPublicProfileUrl",
                            "TYPE": "SOCIAL",
                            "DETAIL": dets['linkedInUrl'],
                            "LABEL": "linkedInPublicProfileUrl"
                           }]

# Add email address if we have one
        if dets['email']<>None:
            c["CONTACTINFOS"].append(
                           {
                            "TYPE": "EMAIL",
                            "DETAIL": dets['email'],
                            "LABEL": "Work"
                           }
                          )


# See if we can find a matching organisation
        c['LINKS']=[]
        l={}
        if self.orgs.has_key(dets['company']):
            c['DEFAULT_LINKED_ORGANISATION']=self.orgs[dets['company']]
            l['ORGANISATION_ID']=self.orgs[dets['company']]
            
        else:
# no match, so add one
            l['ORGANISATION_ID']=self.addOrg(dets['company'])

# add job title
        l['ROLE']=dets['title']
        c['LINKS'].append(l)

# add contact record to crm
        try:
            c=self.crm.addContact(c)
        except urllib2.HTTPError as e:
            print "Error adding contact."
            print e
            print json.dumps(c)
            sys.exit()

# add to in memory list
        self.ins_contacts["%s %s" % (c['FIRST_NAME'],c['LAST_NAME'])] = c['CONTACT_ID']

# Update image
        if dets['pictureUrl']<>None:
            img = urllib2.urlopen(dets['pictureUrl']).read()
            self.addPicture(c['CONTACT_ID'], img)
        
    def addPicture(self, id, picturestream):
        callREST("PUT","/v2.1/Contacts/%s/Image/name.jpg" % str(id), picturestream)

    def addPicturetoName(self, name, picturestream):

# add a picture to a name
        if self.ins_contacts.has_key(name):
            id=self.ins_contacts[name]
            self.addPicture(id, picturestream)
        else:
            print "%s - name not found in Insighly" % name


    def addEmailtoName(self, name, email, label="WORK"):

# add an email to a name
        if self.ins_contacts.has_key(name):
            id=self.ins_contacts[name]
            self.addEmail(id, email, label)
        else:
            print "%s - name not found in Insighly" % name

    def addEmail(self, id, email, label="WORK"):

# add email to an id

# get the record
        c=self.crm.getContact(id)

# add email
        c["CONTACTINFOS"].append({"TYPE": "EMAIL","DETAIL": email,"LABEL": label})

# save
        self.crm.addContact(c)

    def addPhonetoName(self, name, phone, label="WORK"):

# add a phone number to a name
        if self.ins_contacts.has_key(name):
            id=self.ins_contacts[name]
            self.addPhone(id, phone, label)
        else:
            print "%s - name not found in Insighly" % name

    def addPhone(self, id, phone, label="WORK"):

# add phone number to an id

# get the record
        c=self.crm.getContact(id)

# add email
        c["CONTACTINFOS"].append({"TYPE": "PHONE","DETAIL": phone,"LABEL": label})

# save
        self.crm.addContact(c)


    def addOrg(self,name):
        
# add a new organisation          
        c={}
        c['ORGANISATION_NAME']=name
        resp=self.crm.addOrganization(c)

# add to list of organisations in memory
        self.orgs[name]=resp['ORGANISATION_ID']

# return id
        return(resp['ORGANISATION_ID'])


    def load_insightly_orgs(self):

# load org ids from insightly
        o=self.crm.getOrganizations()
        self.orgs={}
        for x in o:
            self.orgs[x['ORGANISATION_NAME']]=x['ORGANISATION_ID']

    def checkDetails(self, id, name, who):

# check for an existing entry if it is in step with linkedIn.
# Extend later. For not it just appends a tag if missing

# get contact details for supplied id
        contact = self.crm.getContact(id)

# create tag to add for owner
        tag={"TAG_NAME" : "LIContact-%s" % who}

# add tag if needed
        if contact.has_key("TAGS"):
            t=contact["TAGS"]
            if tag not in t:
                t.append(tag)
                print "Adding tag %s to %s %s" % (tag, contact['FIRST_NAME'], contact['LAST_NAME'])
                contact["TAGS"]=t
                self.crm.addContact(contact)

# no Tags so add from scrach
        else:
            t=[tag]
            contacts["TAGS"]=t
            self.crm.addContact(contact)


class linkedIn():
#################################
# data and methods for LinkedIn #
#################################

    def __init__(self, token_set, who):

        self.who=who
#################################
# Linked In keys                #
#################################
        CONSUMER_KEY    = token_set['CONSUMER_KEY']
        CONSUMER_SECRET = token_set['CONSUMER_SECRET']
        USER_TOKEN      = token_set['USER_TOKEN']
        USER_SECRET     = token_set['USER_SECRET']

        auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,'http://localhost',permissions=linkedin.PERMISSIONS.enums.values())
        self.lnk = linkedin.LinkedInApplication(auth)
        self.load_linkedin_connections()

# load clean up mappings
        self.cleanup_company={}
        self.cleanup_email={}
        f=open("cleanup_company.txt")
        for line in f.readlines():
            x=line.split(":")
            self.cleanup_company[x[0]]=x[1]
            self.cleanup_email[x[0]]=x[2].strip()
        f.close()

    def load_linkedin_connections(self):

# load connect ids from linked in
        self.lnk_connections={}
        self.lnk_connections_rev={}
#       conns=self.lnk.get_connections(selectors=['id','first-name','last-name'],params={'count':5})['values']
        conns=self.lnk.get_connections(selectors=['id','first-name','last-name'])['values']
        for c in conns:
            self.lnk_connections["%s %s" % (c['firstName'],c['lastName'])] = c['id']
            self.lnk_connections_rev[c['id']] = ["%s %s" % (c['firstName'],c['lastName'])]
            

    def getDetails(self, name):

# for a given name, get the details from LinkedIn

# get id from name
        id=self.lnk_connections[name]

# get details from LinkedIn
        connection_details = self.lnk.get_profile(member_id=id,selectors=['headline','first-name','last-name','summary','positions','siteStandardProfileRequest','pictureUrl','location'])

# format output
        ret={}
        ret['id']=id
        ret['first-name']=connection_details['firstName']
        ret['last-name']=connection_details['lastName']
        ret['company']='Unknown'
        ret['title']=None
        ret['location-area']=None
        ret['location-country']=None
        ret['pictureUrl']=None
        ret['linkedInUrl']=None
        ret['email']=None

        ret['summary']="Linked in says..."
        if connection_details.has_key('summary'):
            ret['summary']=ret['summary'] + "\n\n" + connection_details['summary']
        else:
            ret['summary']=ret['summary'] + "nothing\n"

# Fix private entries in name fields
        if ret['first-name']=="private":
            ret['first-name']=name.split(" ")[0]
            ret['last-name']=" ".join(name.split(" ")[1:])

# update company and position if available
        if connection_details.has_key('positions'):
            if connection_details['positions'].has_key('values'):
                pos=connection_details['positions']['values'][0]
                if pos.has_key('company'):
                    if pos['company'].has_key('name'):
                        ret['company']=pos['company']['name']
                if pos.has_key('title'):
                    ret['title']=pos['title']

# location
        if connection_details.has_key('location'):
            location=connection_details['location']
            if location.has_key('country'):
                if location['country'].has_key('code'):
                    ret['location-country']=location['country']['code']
            if location.has_key('name'):
                    ret['location-area']=location['name']

        if connection_details.has_key('pictureUrl'):
            ret['pictureUrl']=connection_details['pictureUrl']

# linkedIn URL
        if connection_details.has_key('siteStandardProfileRequest'):
            bit=connection_details['siteStandardProfileRequest']
            if bit.has_key('url'):
                ret['linkedInUrl']=bit['url'].split("&")[0]    # only need the id which is the first parameter

# data is a bit crap so we try to clean it up before using it
        self.cleanUp(ret)

        return(ret)

    def cleanUp(self, ret):

# the linkedIn data is shithouse so we try to clean it

# map similar company names to a single name, also add company email if we know it
        for k in self.cleanup_company.keys():
            if ret['company'].find(k)>=0:
                ret['company']=self.cleanup_company[k]
                if self.cleanup_email[k]<>None:
                    ret['email']="%s.%s%s" % (ret['first-name'],ret['last-name'],self.cleanup_email[k])


    def getCheckDetails(self, id):
# simple check for now - can extend it later. Just pass name back as we already have that
# later can extend it to comparing the summary and company
        return(self.lnk_connections_rev[id])

class controller():
###############################################
# processing engine                           #
###############################################

    def __init__(self, crm, linkedIn):
        self.crm=crm
        self.linkedIn=linkedIn
        self.who=self.linkedIn.who
        self.match()
        self.load_exclusions()

    def match(self):

# match the two sets of ids
        print "Looking for matches..."

        self.mapping={}  # maps linkedIn id to CRM id
        self.nomapping=[]  # list of linkedIn id that weren't found - new people

        for k in self.linkedIn.lnk_connections.keys():
            if self.crm.ins_contacts.has_key(k):
                self.mapping[self.linkedIn.lnk_connections[k]] = self.crm.ins_contacts[k]
            else:
                if k<>"private private":
                    self.nomapping.append(k)

    def load_exclusions(self):
        f=open("cleanup_exclude.txt")
        self.exclude=[]
        for line in f.readlines():
            self.exclude.append(line.strip())
        f.close()

    def run(self):

# if there is no mapping then add user unless on the blocked list
        for x in self.nomapping:
            if x not in self.exclude:
                print "Adding new contact: " + x.encode('ascii', 'ignore').decode('ascii')
                self.crm.addContact(self.linkedIn.getDetails(x), self.who)

# If we have a match then check it is still right
        for x in self.mapping.keys():
            self.crm.checkDetails(self.mapping[x], self.linkedIn.getCheckDetails(x), self.who)


#############################################
# These are the keys to connect to LinkedIn #
# and Insightly.                            #
#############################################

marks_keys={'CONSUMER_KEY' : '75157za92khx9s',
         'CONSUMER_SECRET' : 'nBI6vmsyGMZqAop6',
              'USER_TOKEN' : '408d038b-4ad5-4741-a41f-c9dd6b505e9b',
             'USER_SECRET' : '842d9661-7f49-4449-ae5a-ee4751f7a6cc'}

johns_keys={'CONSUMER_KEY' : '75vkdlhutjkjqv',
         'CONSUMER_SECRET' : 'HA3kuROaHI3wJO9B',
              'USER_TOKEN' : '67b87588-9d94-446f-9d40-3972e1b9066f',
             'USER_SECRET' : 'aef27e20-20fb-40d0-9b2d-767175456415'}

tims_keys= {'CONSUMER_KEY' : '753ofe2uqpagc0',
         'CONSUMER_SECRET' : 'dFZkiLYlBNZNf2rC',
              'USER_TOKEN' : '49e5d823-376d-4686-ab76-f138519f5070',
             'USER_SECRET' : 'e6b8cca2-8b87-4f86-b862-b50bb14628c4'}

INSIGHT_KEY='1b59c7a6-98cc-4788-b4ae-d063453e04ab'

if __name__ == "__main__":

    c=crm(INSIGHT_KEY)

    print "Going through Mark's contacts..."
    i=linkedIn(marks_keys, "Mark")
    r=controller(c, i)
    r.run()

    print "Going through John's contacts..."
    i=linkedIn(johns_keys, "John")
    r=controller(c, i)
    r.run()

    print "Going through Tim's contacts..."
    i=linkedIn(tims_keys, "Tim")
    r=controller(c, i)
    r.run()
