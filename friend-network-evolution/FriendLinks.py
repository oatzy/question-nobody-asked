import sys
from urllib2 import urlopen
from xml.etree.ElementTree import ElementTree

screen_name = "oatz" #Change this
friend_ids = []
friend_names = []

def parse_friends():
    print "Getting friends IDs.."
    global friend_ids
    folurl = "https://api.twitter.com/1/friends/ids.xml?screen_name="+screen_name
    root = ElementTree(file=urlopen(folurl))
    iter = root.getiterator()
    for element in iter:
        if element.text:
            if element.tag == "id":
                text = element.text
                friend_ids += [repr(text).replace("'", "")]
                #print repr(text)
    print "Done!"

#If you follow more than 150 people this may fail; API limit
def getNames():
    print "Getting user names.."
    global friend_names
    for user in friend_ids:
        url = "https://api.twitter.com/1/users/lookup.xml?user_id="+user
        #print url
        root = ElementTree(file=urlopen(url))
        iter = root.getiterator()
        for element in iter:
            if element.text:
                if element.tag == "screen_name":
                    text = element.text
                    friend_names += [repr(text).replace("'", "")]
    print "Done!"
                
#This will take AGES to run, O(n^2). Just leave it be.
#Won't find protected connections.
def find_connections():
    print "Getting connections..."
    f = open("connections.txt", "a")
    size = len(friend_names)
    for i in xrange(size):
        print friend_names[i]+"\n"
        for j in xrange(size):
            url = "http://doesfollow.com/"+friend_names[i]+"/"+friend_names[j]
            #print url
            for line in urlopen(url):
                if "Yup" in line:
                    f.write(friend_names[i]+","+friend_names[j]+"\n")
    f.close()
    print "Done!"
    

parse_friends()
getNames()
find_connections()
