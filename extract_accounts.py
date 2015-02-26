f=open("LinkedInExport.html")

def getpart(str, start, offset, end):
    part=str[start + offset:]
    where=part.find(end)
    return(part[:where])

name=None
newname=None
title=None
company=None
location=None

accounts=set()

for line in f.readlines():

# Name

    pos=line.find("contacts-contacts-list-contact_name-0")
    if pos>=0:
        nextbit=getpart(line, pos, 39, "<")
        if nextbit.find("image")<0:
            newname=nextbit

            name=newname


# Company

    pos=line.find('class="company"')
    if pos>=0:
        accounts.add(getpart(line, pos, 16, "<"))

# Print last

for x in accounts:
    print x+","

