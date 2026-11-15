from math import e
import random


#Global Variables
it = 96 #total iterations
tp = 3 #through-put; serve rate
n = 10 #total tables
st = 5 #average length of stay
T = 0 #time tracker


#Classes
class Poisson:

    def __init__(self):
        self.dist = []

    def setDist(self, mu):
        for x in xrange(7):
            self.dist += [[x,po(mu,x)]]

    def printDist(self):
        for i in self.dist:
            print i

    def update(self, T):
        self.dist = []
        time = (T/12.0)+9
        mu = no(time)
        self.setDist(mu)

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

    def addCustomers(self, p,p1):
        c = p.getRand()
        for i in xrange(c):
            self.que += [[p1.getRand()+1,0]]

    def clean(self):
        temp = []
        for i in self.que:
            if i[0] != 0:
                temp += [i]
        self.que = temp

    def update(self):
        for i in self.que:
            if i[0] == 1:
                i[1] += 1

    def serve(self, tp):
        if len(self.que)<=tp:
            self.que = []
        else:
            for i in xrange(tp):
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

    def clearTables(self, st):
        for i in self.tables:
            if i[1] >= st:
                i[0],i[1] = 0,0

    def clearAll(self):
        for i in self.tables:
            i[0],i[1]  = 0,0

    def update(self):
        for i in self.tables:
            if i[0] == 1:
                i[1] += 1

    def inUse(self):
        count = 0
        for i in self.tables:
            if i[0] == 1:
                count += 1
        return count

    def seat(self):
        self.tables[self.tables.index([0,0])][0] = 1


#General Functions
def factorial(a):
    b = 1
    while a > 0:
        b *= a
        a -= 1
    return b

def po(mu,x): #poisson
    return (e**(-mu)*mu**x)/factorial(x)

def no(t): #normal dist
    return (1.77308)*e**(-(0.154321)*(t-12)**2)

#Main Function
def main(t, q, p, it, st, tp, n, T):
    # temp variables
    w = 0
    maxq = [0,0]
    q0size,qsize,tsize,waiting = [],[],[],[]
    wait = Queue()
    p1 = Poisson()
    p1.setDist(0.75)
    # start loop
    for x in xrange(it):
        w1 = 0
        # updates
        p.update(T)
        wait.update()
        t.update()
        t.clearTables(st)
        # if tables; seat anyone waiting
        while w!=0 and t.inUse() != n:
            t.seat()
            wait.unload()
            w -= 1
        # update queue
        q.update()
        if maxq[0] < q.findMax():
            maxq[0] = q.findMax()
        q.addCustomers(p,p1)
        q0size += [len(q.que)]
        # serve; variable groups size
        if q.size() < tp:
            s = q.size()
        else:
            s = tp
        j = 0
        while s != 0:
            if q.que[j][0] != 0:
                q.que[j][0]-=1
                s -=1
            else:
                j+=1
        for i in q.que:
            if i[0] == 0:
                w1 += 1
        q.clean()
        # if tables; seat just served
        while w1!=0 and t.inUse() != n:
            t.seat()
            w1 -= 1
        # add anyone without seat to 'waiting'
        if w1 > 0:
            for i in xrange(w1):
                wait.que += [[1,0]]
        # incriment
        w += w1
        T += 1
        # update trackers & maxes
        qsize += [len(q.que)]
        tsize += [t.inUse()]
        waiting += [w]
        if maxq[1] < wait.findMax():
            maxq[1] = wait.findMax()
        # tidy
        wait.clean()
    # outputs
    print maxq
    print q0size
    print tsize
    print qsize
    print waiting

#Start
p = Poisson()

t = Room()
t.setTables(n)

q = Queue()

main(t, q, p, it, st, tp, n, T)
