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

for line in f.readlines():

# Name

    pos=line.find("contacts-contacts-list-contact_name-0")
    if pos>=0:
        nextbit=getpart(line, pos, 39, "<")
        if nextbit.find("image")<0:
            newname=nextbit

# Print it - if we have a new name

            if name<>None:
                out="%s,%s,%s,%s" % (name, title, company, location)
                out = out.replace("&amp;","&")
                print out
            name=newname

# Title

    pos=line.find('class="title"')
    if pos>=0:
        title=getpart(line, pos, 14, "<")

# Company

    pos=line.find('class="company"')
    if pos>=0:
        company=getpart(line, pos, 16, "<").replace(",","-")

# Location

    pos=line.find('class="location"')
    if pos>=0:
        location=getpart(line, pos, 17, "<").replace(",","-")

# Print last

out="%s,%s,%s,%s" % (name, title, company, location)
out = out.replace("&amp;","&")
print out

