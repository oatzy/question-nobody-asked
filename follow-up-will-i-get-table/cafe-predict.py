from math import e
import random


#Global Variables
it = 1000 #total iterations
tp = 7 #through-put; serve rate
st = 5 #average stay time
n = 16 #total tables
u = 16 #tables in use
q = 4 #people ahead of you in queue
d = 2 #number of drinks ordered
ss = 5 #duration of one iteration (in mins)


#Classes
class Poisson:

    def __init__(self):
        self.dist = []

    def setDist(self, mu):
        for x in xrange(9):
            self.dist += [[x,po(mu,x)]]

    def getRand(self):
        s = self.dist
        i = 0
        w = s[0][1]
        r = random.random()
        while r>=w:
            i +=1
            if i > 7:
                i,r=8,0
            w += s[i][1]
        return i


class Queue:

    def __init__(self):
        self.que = []

    def fillRand(self, n, p):
        for i in xrange(n):
            self.que += [[p.getRand()+1,0]]

    def clean(self):
        temp = []
        for i in self.que:
            if i[0] != 0:
                temp += [i]
        self.que = temp

    def serve(self, tp):
        if self.size() < tp:
            s = self.size()
        else:
            s = tp
        j = 0
        while s != 0:
            if self.que[j][0] != 0:
                self.que[j][0]-=1
                s -=1
            else:
                j+=1

    def served(self):
        w = 0
        for i in self.que:
            if i[0] == 0:
                w += 1
        return w

    def seated(self):
        x = 0
        for i in self.que:
            if i[0] == 0 and i[1] == 1:
                x += 1
        return x

    def size(self):
        temp = 0
        for i in self.que:
            temp += i[0]
        return temp


class Room:

    def __init__(self):
        self.tables = []

    def setTables(self, n):
        self.tables = [[0,0] for i in xrange(n)]

    def fillRand(self, n,p):
        for i in xrange(n):
            self.tables[i][0] = 1
            self.tables[i][1] = p.getRand()-random.randint(0,4)+2

    def clearTables(self):
        for i in self.tables:
            if i[1] <= 0:
                i[0],i[1] = 0,0

    def update(self):
        for i in self.tables:
            if i[0] == 1:
                i[1] -= 1

    def inUse(self):
        count = 0
        for i in self.tables:
            if i[0] == 1:
                count += 1
        return count

    def hold(self):
        self.tables[self.tables.index([0,0])] = [2,0]

    def seat(self,p):
        self.tables[self.tables.index([0,0])] = [1,p.getRand()+2]


#General Functions

def average(s):
    return float(sum(s))/len(s)
        
def factorial(a):
    b = 1
    while a > 0:
        b *= a
        a -= 1
    return b

def po(mu,x): #poisson
    return (e**(-mu)*mu**x)/factorial(x)

#Main Function
def main(q,n,u,d,tp,st,tbls,wts):
    #initialise
    T,h = 0,0
    p = Poisson()
    p.setDist(0.75) #orders size dist
    r = Poisson()
    r.setDist(3.5) #stay distribution
    Q = Queue()
    Q.fillRand(q,p)
    Q.que += [[d,0]] #join back of queue
    t = Room()
    t.setTables(n)
    t.fillRand(u,r)
    W = 0 #waiting tracker
    while q > 0:
        #update tables
        t.update()
        t.clearTables()
        #seat waiting
        while W != 0 and t.inUse() != n:
            t.seat(r)
            W -= 1
        #table saving
        for i in Q.que:
            if t.inUse() != n and i[0] > 1 and i[1] != 1:
                if random.Random() <= float(u)/n:
                    t.hold()
                    i[1] = 1
        if Q.que[-1][1] == 1: #did you save a table?
            h = 1
        #serve
        Q.serve(tp)
        w=Q.served()-Q.seated()
        #seat people with held tables
        for i in xrange(Q.seated()):
            t.tables[self.tables.index([2,0])] = [0,0]
            t.seat(r)
        Q.clean()
        # if tables; seat served w/o saved tables
        while w!=0 and t.inUse() != n:
            t.seat(r)
            w -= 1
        #update trackers
        q = len(Q.que)
        T += 1
        W += w
    #loop trackers
    if W == 0:
        h = 1
    tbls += [(n-t.inUse()+h)]
    wts += [T]
        

#Start
tbls,wts = [],[]
for i in xrange(it):
    main(q,n,u,d,tp,st,tbls,wts)
#output averages
print str(int(average(tbls)))+" tables available"
print str(100*(it-tbls.count(0))/float(it))+"% chance of a table"
print "Queing time ~ "+str(round(average(wts)*5))+"mins"
