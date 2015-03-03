from insightly import Insightly
import json
import requests
import base64

url='https://api.insight.ly'
apikey='1b59c7a6-98cc-4788-b4ae-d063453e04ab'
base64string = base64.encodestring('%s:%s' % (apikey, '')).replace('\n', '')
h = "Basic %s" % base64string
hdr = {'Authorization' : h }

## Get a contact
full_url= url + "/v2.1/contacts/104251444"

r = requests.get(full_url,  headers=hdr)

print(r.status_code)
#print(r.text)
print(r.content)

x=r.content

x["FIRST_NAME"]="Updated"

## Update contact with a Put

full_url= url + "/v2.1/contacts/"


#payload=open("andrea.jpg")

#payload={'filename' : 'http://s3.amazonaws.com/insightly.userfiles/462614/MW5KVO/3a6ab14a-177a-486e-bdb5-e49b4c39ae93.jpg'}
#payload={'filename' : 'andrea.jpg'}

#full_url= url + "/v2.1/Contacts/103192436/Image/"

#r = requests.post(full_url, files={'file': open('andrea.jpg','rb')}, headers=hdr)
#r = requests.post(full_url, params=payload, files={'file': 'andrea.jpg'}, headers=hdr)
#r = requests.post(full_url, params=payload, files={'file': "('andrea.jpg', open('andrea.jpg,'rb'), 'Content-Type: image/jpeg')"}, headers=hdr)

##print(r.status_code)
#print(r.text)
#print(r.content)

#contact = i.getContact(103192436)

#for x in contact.keys():
#    print "%s: %s" % (x, contact[x])

