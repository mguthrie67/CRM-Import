#!/bin/env python
# pip install insightly-python
# pip install python-linkedin

import json
from linkedin import linkedin
from insightly import Insightly

class crm():
################################
# data and methods for the crm #
################################

    def __init__(self, insight_key):
        self.crm = Insightly(apikey=insight_key)
        self.load_insightly_contacts()
        self.load_insightly_orgs()

    def load_insightly_contacts(self):
###################################
# load contact ids from insightly #
###################################
        self.ins_contacts = {}
        conns = self.crm.getContacts()
        for c in conns:
            self.ins_contacts["%s %s" % (c['FIRST_NAME'],c['LAST_NAME'])] = c['CONTACT_ID']

    def addContact(self,dets,who):
###################################
# add a new contact, also a new   #
# org if required                 #
###################################
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

        c['IMAGE_URL']=dets['pictureUrl']

        linkedinurl="https://www.linkedin.com/profile/view?%s" % dets['id']

        c["CONTACTINFOS"]=[{"SUBTYPE": "LinkedInPublicProfileUrl",
                            "TYPE": "SOCIAL",
                            "DETAIL": linkedinurl,
                            "LABEL": "LinkedInPublicProfileUrl"
                           }]
        if dets['email']<>None:
            c["CONTACTINFOS"].append(
                           {
                            "TYPE": "EMAIL",
                            "DETAIL": dets['email'],
                            "LABEL": "Work"
                           }
                          )

        print c

        # find org
        c['LINKS']=[]
        l={}
        if self.orgs.has_key(dets['company']):
            c['DEFAULT_LINKED_ORGANISATION']=self.orgs[dets['company']]
            l['ORGANISATION_ID']=self.orgs[dets['company']]
        else:
#            c['DEFAULT_LINKED_ORGANISATION']=self.addOrg(dets['company'])
            l['ORGANISATION_ID']=self.addOrg(dets['company'])
            self.orgs[dets['company']]=l['ORGANISATION_ID']
            print self.orgs
        l['ROLE']=dets['title']
        c['LINKS'].append(l)

        self.crm.addContact(c)

    def addOrg(self,name):
###################################
# add a new organisation          #
###################################
        c={}
        c['ORGANISATION_NAME']=name
        resp=self.crm.addOrganization(c)
        return(resp['ORGANISATION_ID'])

###################################
# load org ids from insightly     #
###################################
    def load_insightly_orgs(self):
        o=self.crm.getOrganizations()
        self.orgs={}
        for x in o:
            self.orgs[x['ORGANISATION_NAME']]=x['ORGANISATION_ID']

    def checkDetails(self, id, name, who):
#        print "*************************************************************************\n\n"
        contact = self.crm.getContact(id)
#        print json.dumps(contact, indent=3)
        tag={"TAG_NAME" : "LIContact-%s" % who}
        if contact.has_key("TAGS"):
            t=contact["TAGS"]
            if tag not in t:
                t.append(tag)
                print "Adding tag %s to %s" % (tag, who)
            contact["TAGS"]=t
        else:
            t=[tag]
            contacts["TAGS"]=t
#        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
#        print json.dumps(contact, indent=3)
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
###################################
# load connect ids from linked in #
###################################
        self.lnk_connections={}
        self.lnk_connections_rev={}
#       conns=self.lnk.get_connections(selectors=['id','first-name','last-name'],params={'count':5})['values']
        conns=self.lnk.get_connections(selectors=['id','first-name','last-name'])['values']
        for c in conns:
            self.lnk_connections["%s %s" % (c['firstName'],c['lastName'])] = c['id']
            self.lnk_connections_rev[c['id']] = ["%s %s" % (c['firstName'],c['lastName'])]

    def print_connections(self):
        connection_id = self.lnk_connections['values'][4]['id']
        connection_details = self.lnk.get_profile(member_id=connection_id,selectors=['headline','first-name','last-name','summary','positions','siteStandardProfileRequest','pictureUrl','location'])
        print json.dumps(connection_details, indent=1)

    def getDetails(self, name):
        id=self.lnk_connections[name]
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
            ret['summary']="nothing\n"
        ret['summary']=ret['summary'] + "\n- - - - - - - - - - -\n\n"

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

        self.cleanUp(ret)

        return(ret)

    def cleanUp(self, ret):
##########################################################
# the linkedIn data is shithouse so we try to clean it   #
##########################################################
        print ret['company']
        for k in self.cleanup_company.keys():
            if ret['company'].find(k)>=0:
                print "1"
                ret['company']=self.cleanup_company[k]
                if self.cleanup_email[k]<>None:
                    print "2"
                    ret['email']="%s.%s%s" % (ret['first-name'],ret['last-name'],self.cleanup_email[k])

    def getCheckDetails(self, id):
# simple check for now - can extend it later. Just pass name back as we already have that
# later can extend it to comparing the summary and company
        return(self.lnk_connections_rev[id])

class controller():

    def __init__(self, crm, linkedIn):
        self.crm=crm
        self.linkedIn=linkedIn
        self.who=self.linkedIn.who
        self.match()

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

    def run(self):
        for x in self.nomapping:
            print "Adding new contact: " + x.encode('ascii', 'ignore').decode('ascii')
            self.crm.addContact(self.linkedIn.getDetails(x), self.who)
        for x in self.mapping.keys():
            self.crm.checkDetails(self.mapping[x], self.linkedIn.getCheckDetails(x), self.who)

# for each person:
# 1) load linked in contacts - this will be a subset of all of our contacts
# 2) load crm contacts - this should be the whole list of our contacts
# 3) go through the linked in contacts and see if we have a match in the CRM
#   a) no match - add it
#   b) match - check if the summary matches, if not update it

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
