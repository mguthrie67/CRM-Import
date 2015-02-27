# pip install insightly-python
# pip install python-linkedin

import json
from linkedin import linkedin
from insightly import Insightly

class crm_updater():

    def __init__(self, token_set):

#################################
# Linked In keys                #
#################################
        CONSUMER_KEY    = token_set['CONSUMER_KEY']
        CONSUMER_SECRET = token_set['CONSUMER_SECRET']
        USER_TOKEN      = token_set['USER_TOKEN']
        USER_SECRET     = token_set['USER_SECRET']

#################################
# Insightly keys                #
#################################
        INSIGHT_KEY=token_set['INSIGHT_KEY']

#################################
# Create connections to both    #
#################################
        self.crm = Insightly(apikey=INSIGHT_KEY)

        auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,'http://localhost',permissions=linkedin.PERMISSIONS.enums.values())

        self.lnk = linkedin.LinkedInApplication(auth)

    def load_linkedin_connections(self):
###################################
# load connect ids from linked in #
###################################
        self.lnk_connections={}
        conns=self.lnk.get_connections(selectors=['id','first-name','last-name'],params={'count':5})['values']
        for c in conns:
            print c
            print c['firstName']
            self.lnk_connections["%s %s" % (c['firstName'],c['lastName'])] = c['id']

        print self.lnk_connections


    def load_insightly_contacts(self):
###################################
# load contact ids from insightly #
###################################
        self.ins_contacts = {}
        conns = self.crm.getContacts()
#        print json.dumps(self.ins_contacts, indent=3 )
        for c in conns:
            self.ins_contacts["%s %s" % (c['FIRST_NAME'],c['SECOND_NAME'])] = c['CONTACT_ID']

    def match_ids(self):
####################################
# match ids across systems         #
####################################


    def print_connections(self):
        connection_id = self.lnk_connections['values'][4]['id']
        connection_details = self.lnk.get_profile(member_id=connection_id,selectors=['headline','first-name','last-name','summary','positions','siteStandardProfileRequest','pictureUrl','location'])
        print json.dumps(connection_details, indent=1)

#    def add_comment(self, connection_id):


marks_keys={'CONSUMER_KEY' : '75157za92khx9s',
         'CONSUMER_SECRET' : 'nBI6vmsyGMZqAop6',
              'USER_TOKEN' : '408d038b-4ad5-4741-a41f-c9dd6b505e9b',
             'USER_SECRET' : '842d9661-7f49-4449-ae5a-ee4751f7a6cc',
             'INSIGHT_KEY' :'1b59c7a6-98cc-4788-b4ae-d063453e04ab'}

update=crm_updater(marks_keys)
update.load_linkedin_connections()
#update.print_connections()
#update.load_insightly_contacts()