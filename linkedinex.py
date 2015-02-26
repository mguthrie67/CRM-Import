CONSUMER_KEY = '75157za92khx9s'
CONSUMER_SECRET = 'nBI6vmsyGMZqAop6'
USER_TOKEN = '408d038b-4ad5-4741-a41f-c9dd6b505e9b'
USER_SECRET = '842d9661-7f49-4449-ae5a-ee4751f7a6cc'
RETURN_URL="http://localhost"
import json
from linkedin import linkedin

auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL,permissions=linkedin.PERMISSIONS.enums.values())

app = linkedin.LinkedInApplication(auth)

connections = app.get_connections()

linkedin_contacts = 'contacts.json'

f = open(linkedin_contacts, 'w')
f.write(json.dumps(connections, indent=1))
f.close()