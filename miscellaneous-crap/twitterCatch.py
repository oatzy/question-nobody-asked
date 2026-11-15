import twitter
import math

hath = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
monName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
dayName = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
dayLong = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
monLong = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
dateSuf = ["st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "st"]

user1 = "Oatz"
user2 = "PkmnTrainerJ"

#username="_username_", password="_password_"

api = twitter.Api()

def disclaimer():
    print "The calculation is based on the assumtion that a user tweets"
    print "at an aproximately constant rate, per day."
    print "\n The 'average tweet rate' is based on when the first and last"
    print "of a user's last 200 tweets were tweeted (which isn't ideal)"
    print "\n Because of these things, the output of this program"
    print "are just estimations, and should be taken with a pinch of salt."

def timeDif(x, y):
    mon1, mon2 = x[1], y[1]
    day1, day2 = int(x[2]), int(y[2])
    x = x[3].split(":")
    y = y[3].split(":")
    hr1 = float(x[0])+(float(x[1])/60)+(float(x[2])/3600)
    hr2 = float(y[0])+(float(y[1])/60)+(float(y[2])/3600)
    if mon1 != mon2:
        dmon = hath[monName.index(mon2)]
        dday = dmon + day1 - day2
    else:
        dday = day1-day2
    dday += (hr1-hr2)/24.0
    return dday


def dayLead(days, cur):
    day = dayLong[(dayName.index(cur[0])+days)%7]
    days += int(cur[2])
    while days > hath[monName.index(cur[1])]:
        days -= hath[monName.index(cur[1])]
        if monName.index(cur[1]) == 1:
            cur[-1] = str(int(cur[-1]+1))
            cur[1] = "Jan"
        else:
            cur[1] = monName[monName.index(cur[1])+1]
    return [day, monLong[monName.index(cur[1])], str(days), cur[-1]]


def Calc(user1, user2):
    
    U1tweets = api.GetUser(user1).statuses_count
    U2tweets = api.GetUser(user2).statuses_count

    dtweets = U2tweets - U1tweets

    U1stats = api.GetUserTimeline(user=user1, count="200")
    U2stats = api.GetUserTimeline(user=user2, count="200")

    U1f = U1stats[0].created_at.split(" ")
    U1l = U1stats[-1].created_at.split(" ")
    U2f = U2stats[0].created_at.split(" ")
    U2l = U2stats[-1].created_at.split(" ")

    dtime1 = timeDif(U1f, U1l)
    dtime2 = timeDif(U2f, U2l)

    U1rate = len(U1stats)/dtime1
    U2rate = len(U2stats)/dtime2

    drate = U1rate-U2rate

    if dtweets < 0:
        print "You're already "+str(dtweets*-1)+" tweets ahead of @" + user2
        if U2rate > U1rate:
            days = int(math.ceil(dtweets/drate))
            "But they will catch up to you in " +str(days) + " days."
            date = dayLead(days, U2f)
            print "Or, by " + date[0] +", "+ date[1] +" "+ date[2]+dateSuf[int(date[2])-1]+", "+date[3]
        else:
            print "And they're unlikely to catch up"
    elif dtweets == 0:
        print "You're level pegging"
        if U2rate > U1rate:
            print "But @" + user2 + " is going to overtake you."
        elif U1rate > U2rate:
            print "But you're going to take the lead."
    elif drate <= 0:
        print "@"+user2+" is tweeting faster than you."
        print "You'd need at least " + str(int(math.ceil(U2rate)+1)) + " tweets/day to catch up."
        print "That's about " + str(int(math.ceil(U2rate-U1rate+1))) + " more than you're currently tweeting/day."
    else:
        days = int(math.ceil(dtweets/drate))
        print "You should catch up to @"+user2+" in " + str(days) + " days."
        date = dayLead(days, U1f)
        print "Or, by " + date[0] +", "+ date[1] +" "+ date[2]+dateSuf[int(date[2])-1]+", "+date[3]


def catchUp(user1, user2):
    if api.GetUser(user1).protected:
        print "Your account is protected. Couldn't complete calculation."
    elif api.GetUser(user2).protected:
        print "@"+user2+"'s account is protected. Couldn't complete calculation."
    else:
        Calc(user1, user2)

catchUp(user1, user2)
