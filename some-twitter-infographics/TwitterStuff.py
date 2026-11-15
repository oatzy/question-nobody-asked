import sys
from urllib2 import urlopen
from xml.etree.ElementTree import ElementTree
from time import gmtime

screen_name = "oatz" #Change this
friend_ids = ["20190060"] #My userid; change as well

hath = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
monName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def Days(date):
    date = date.split()
    curr = gmtime()
    dMon = monName.index(date[1])
    monDays = 0
    for i in xrange(0, dMon):
        monDays += hath[i]
    monDays += int(date[2])
    days = curr.tm_yday - monDays
    days += 365*(curr.tm_year - int(date[-1]))
    return days

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
    print "Done!"

#If you follow more than 150 people this may fail; API limit
def getStuff():
    print "Getting user names and stuff.."
    date = gmtime()
    filename = "twitterdata-{}{}{}.txt".format(date.tm_year,date.tm_mon,date.tm_mday)
    f = open("descriptions.txt", "w")
    g = open(filename, "w")
    g.write("Screen Name,Days Online,Tweet Count,Average Tweet Rate\n")
    for user in friend_ids:
        url = "https://api.twitter.com/1/users/lookup.xml?user_id="+user
        root = ElementTree(file=urlopen(url))
        iter = root.getiterator()
        for element in iter:
            if element.text:
                if element.tag == "screen_name":
                    text = element.text
                    print text
                    g.write("{},".format(repr(text).replace("'", "")))
                    f.write("{}\n".format(repr(text).replace("'", "")))
                if element.tag == "description":
                    text = element.text
                    f.write(repr(text).replace("'", "")+"\n")
                if element.tag == "created_at":
                    text = element.text
                    days = Days(repr(text).replace("'", ""))
                    g.write("{},".format(days))
                if element.tag == "statuses_count":
                    text = element.text
                    statuses = repr(text).replace("'", "")
                    g.write("{},{}\n".format(statuses,float(statuses)/days))
        #g.write(outstring)
    f.close()
    g.close()
    print "Done!"
    

parse_friends()
getStuff()
