from time import gmtime

hath = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
monName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def Days(date):
    curr = gmtime()
    dMon = monName.index(date[1])
    monDays = 0
    for i in xrange(0, dMon):
        monDays += hath[i]
    monDays += int(date[2])
    days = curr.tm_yday - monDays
    days += 365*(curr.tm_year - int(date[-1]))
    print days


date = "Sun Aug 30 20:07:20 +0000 2011".split()
Days(date)
