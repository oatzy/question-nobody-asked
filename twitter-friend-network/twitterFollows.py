import twitter

api = twitter.Api(username="your_username", password="your_password")

def func():
    Friends = api.GetFriends(user="oatz")
    Fnum = len(Friends)
    nameFriends = [Friends[i].screen_name for i in xrange(Fnum)]
    for j in xrange(Fnum):
        fFriends = api.GetFriends(user=nameFriends[j])
        for k in xrange(Fnum):
            if Friends[k] in fFriends:
                print nameFriends[j] + " " + nameFriends[k]

func()
    
