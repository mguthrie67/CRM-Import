from insightly import Insightly
import json

i = Insightly(apikey='1b59c7a6-98cc-4788-b4ae-d063453e04ab')
#users = i.test()

#contacts = i.getContacts(orderby='DATE_UPDATED_UTC desc')

#print json.dumps(contacts, indent=3 )



contact = i.addContact('sample')
#contact = i.getContact(103192387)
print json.dumps(contact, indent=3)
#contact = i.addOrganization('sample')
#print json.dumps(contact, indent=3)

#org=i.getOrganizations()
#print org

#c={}
##c['CONTACT_ID']=0
#c['FIRST_NAME']="AAAAAAAAA"
#c['LAST_NAME']="BBBBBBBBB"
#i.addContact(c)

#contact = i.getContact(103192436)

#for x in contact.keys():
#    print "%s: %s" % (x, contact[x])

#contact["BACKGROUND"]="Seedy Reidy\n\n1234\n"

#print "\n\n@@@@@@@@@@@@@@@@@@@@@@\n\n"

#for x in contact.keys():
#    print "%s: %s" % (x, contact[x])

#rc = i.addContact(contact)


#rc = i.addPicture(103192436, "andrea.jpg")