import random as rand

#non-shuffled shifts
Dbase = [1,1,1,1,0,0,0]
Mbase = [1,1,0,0,0,0,0]
Nbase = [1,1,1,1,1,0,0]

def hols(S, h):
    for i in xrange(h):
        r = rand.randint(0,363)
        while S[r] != 1:
            r=(r+1)%363
        S[r] = 0
    return S

def holWeeks(S,h):
    for i in xrange(h):
        r = rand.randint(0,51)
        while S[7*r] != 1:
            r = (r+1)%51
        for j in xrange(7):
            S[7*r + j] = 0
    return S

def setUp(D,M,N):
    #year setup
    for i in xrange(52):
        rand.shuffle(Dbase)
        D += Dbase
        rand.shuffle(Mbase)
        M += Mbase
        N += Nbase
    #set up holidays
    D = hols(D,32)
    M = hols(M, 27)
    N = holWeeks(N, 13)
    N = hols(N, 10)

def pickUp(D,M,N):
    count = 0
    for i in xrange(364):
        if D[i] == 1 and N[i] == 1:
            if M[i] == 1 or M[i-1] == 1:
                if rand.random() <= 0.9:
                    count += 1
    return count

def hist(S):
    #generate histogram
    a,b = min(S),max(S)
    h = []
    for i in xrange(a,b+1):
        h += [S.count(i)]
    return h

def average(S):
    return sum(S)/float(len(S))
    
#main
counts = []
for i in xrange(10000):
    D = []
    M = []
    N = []
    setUp(D,M,N)
    counts += [pickUp(D,M,N)]
print min(counts)
print max(counts)
print hist(counts)
print average(counts)
