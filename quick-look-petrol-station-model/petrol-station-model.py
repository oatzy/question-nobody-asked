from math import e
import random


#Global Variables
it = 96 #total iterations
tp = 2 #through-put; serve rate
n = 12 #total pumps
st = 1 #average length of stay
T = 0 #time tracker
ar = 2 #average arrival rate
reps = 100 #number of times to run sim

#Classes
class Poisson:

    def __init__(self):
        self.dist = []

    def setDist(self, mu):
        for x in xrange(8):
            self.dist += [[x,po(mu,x)]]

    def printDist(self):
        for i in self.dist:
            print i

    def getRand(self):
        s = self.dist
        i = 0
        w = s[0][1]
        r = random.random()
        while r>=w:
            i +=1
            if i > 6:
                i,r=7,0
            w += s[i][1]
        return i


class Queue:

    def __init__(self):
        self.que = []

    def clean(self):
        temp = []
        for i in self.que:
            if i[0] != 0:
                temp += [i]
        self.que = temp

    def update(self,S):
        for i in xrange(S.size):
            if S.pumps[i][0] == 1 and S.pumps[i][1] <= 0:
                S.pumps[i] = [2,0]
                self.que += [[i+1,0]]

    def serve(self, S, tp):
        if len(self.que)<=tp:
            for i in self.que:
                S.pumps[i[0]-1] = [0,0]
            self.que = []
        else:
            for i in xrange(tp):
                S.pumps[self.que[i][0]-1] = [0,0]
                self.que[i][0] = 0
            self.clean()

    def findMax(self):
        m = 0
        for i in self.que:
            if i[1] > m:
                m = i[1]
        return m

    def unload(self):
        for i in self.que:
            if i[0] == 1:
                i[0] = 0
                break


class Station:

    def __init__(self):
        self.pumps = []
        self.size = 0

    def setPumps(self, n):
        self.pumps = [[0,0] for i in xrange(n)]
        self.size = n

    def clearPumps(self):
        for i in self.pumps:
            if i[1] <= 0:
                i = [0,0]

    def clearAll(self):
        for i in self.pumps:
            i  = [0,0]

    def update(self):
        for i in self.pumps:
            if i[0] == 1:
                i[1] -= 1

    def inUse(self):
        count = 0
        for i in self.pumps:
            if i[0] > 0:
                count += 1
        return count

    def occupy(self,st):
        self.pumps[self.pumps.index([0,0])] = [1,st]


#General Functions
def factorial(a):
    b = 1
    while a > 0:
        b *= a
        a -= 1
    return b

def po(mu,x): #poisson
    return (e**(-mu)*mu**x)/factorial(x)

def average(s, t):
    for i in xrange(len(s)):
        s[i] = round(s[i]/float(t),2)
    return s


#Main Function
def main(S,Q,p,it,tp,st,P_set,W_set,Q_set):
    T = 0
    W = 0
    for i in xrange(it):
        S.update()
        Q.update(S)
        Q.serve(S,tp)
        W += p.getRand()
        while S.inUse() < S.size and W > 0:
            S.occupy(st)
            W -= 1
        P_set[T] += S.inUse()
        W_set[T] += W
        Q_set[T] += len(Q.que)
        T += 1

#Start
p = Poisson()
p.setDist(ar)

S = Station()
S.setPumps(n)

Q = Queue()
P_set = [0 for i in xrange(it)]
W_set = [0 for i in xrange(it)]
Q_set = [0 for i in xrange(it)]

for j in xrange(reps):
    main(S,Q,p,it,tp,st,P_set,W_set,Q_set)
print P_set
print W_set
print Q_set
