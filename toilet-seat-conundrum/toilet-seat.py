# seat up = 1; down = 0
# male = 1; female =0

import random
from math import e

Toilets = [0, 0, 0]
House = []
totalvisits = 0
mchanges = 0
wchanges = 0

class Person:

    def __init__(self, gender, visits, pu):
        self.gender = gender
        if gender == 0:
            self.up = 0
        else:
            self.up = int(pu*visits)
        self.down = visits-self.up
        self.visitset = []
        self.changecount = 0

    def visit(self,toilet):
        mode = random.choice(self.visitset)
        if Toilets[toilet] != mode:
            self.changecount += 1
        Toilets[toilet] = mode

    def visitAlt(self):
        mode = random.choice(self.visitset)
        if mode == 1:
            self.changecount += 2

    def setVisits(self):
        t = setDist(self.down)
        d = getRand(t)
        if self.gender == 0:
            for i in xrange(d):
                self.visitset += [0]
        else:
            t = setDist(self.up)
            u = getRand(t)
            for i in xrange(d):
                self.visitset += [0]
            for i in xrange(u):
                self.visitset += [1]

    def getVisits(self):
        return len(self.visitset)

    def getGender(self):
        return self.gender

    def getCount(self):
        return self.changecount
        

def factorial(a):
    b = 1
    while a > 0:
        b *= a
        a -= 1
    return b

def setDist(mu):
    dist = {}
    for x in xrange(20):
        dist[x] = (e**(-mu)*mu**x)/factorial(x)
    return dist

def getRand(dist):
    i = 0
    w = dist[0]
    r = random.random()
    while r>=w:
        i +=1
        if i > 19:
            i,r=20,0
        w += dist[i]
    return i

def main():
    global mchanges
    global wchanges
    for i in xrange(totalvisits):
        rp = random.choice(House)
        rt = random.randint(0,2)
        rp.visit(rt)
        #rp.visitAlt()
    for i in House:
        if i.getGender() == 1:
            mchanges += i.getCount()
        elif i.getGender() == 0:
            wchanges += i.getCount()

def setup():
    global totalvisits
    totalvisits = 0
    for i in House:
        while len(i.visitset) == 0:
            i.setVisits()
    for i in House:
        totalvisits += i.getVisits()

for i in xrange(10000):
    House = [Person(0, 5, 0), Person(0, 7, 0), Person(1, 5, 0.9), Person(1, 7, 0.8)]
    setup()
    main()
    
print "M: {}, F: {}".format(mchanges, wchanges)
    
