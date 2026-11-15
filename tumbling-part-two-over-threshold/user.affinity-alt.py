import random as r

#Counters
Likes = 0
Reblogs = 0


class User:

    def __init__(self):
        self.like = 11
        self.reblog = 11

    def setThresholds(self):
        #generated randomly by uniform dist
        self.like = r.uniform(1,11)
        self.reblog = r.uniform(self.like, 11)

    def doesReblog(self, rating):
        return (rating >= self.reblog)
    
    def doesLike(self, rating):
        return (rating >= self.like and not self.doesReblog(rating))

    def rate(self, post):
        #generated randomly by normal dist
        rating = -1
        while rating > 10 or rating < 0:
            rating = post.randomRating()
        return rating


class Post:

    def __init__(self, mu=0, sd=1):
        self.mu = mu
        self.sd = sd

    def randomRating(self):
        return r.gauss(self.mu,self.sd)
        

def simulation(users, picture):
    global Likes
    global Reblogs
    for i in xrange(users):
        u = User()
        u.setThresholds()
        rating = u.rate(picture)
        Likes += u.doesLike(rating)
        Reblogs += u.doesReblog(rating)

pic = Post(5,3)
simulation(100000, pic)
print Likes
print Reblogs
