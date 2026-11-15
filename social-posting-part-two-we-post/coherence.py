import random

#Globals
M = [[0,1,0,0], [1,0,1,1], [0,1,0,1], [0,1,1,0]]
W = [[0,-1,0.5,0.5], [0.3,0,0.7,0], [1.0/3,1.0/3,0,1.0/3], [0.7,0,0.3,0]]
N = len(M)
T = {0: [1,0,1,1]}
E = [1, 1, 1, 1]
alpha = [1.5, 1.25, 0.375, 1.25]
beta = [0, 0, 0, 0]

def setW():
    W = [[0 for i in xrange(N)] for j in xrange(N)]
    for i in xrange(N):
        for j in xrange(N):
            W[i][j] = M[i][j]/float(sum(M[i]))
    return W

def randomM(N):
    M = [[random.randint(0,1) for i in xrange(N)] for j in xrange(N)]
    for i in xrange(N):
        M[i][i] = 0
    return M

def dot(m, t, u):
    temp = 0
    for i in xrange(N):
        temp += m[u][i]*t[i]
    #temp = int(temp >= 0.5)
    return temp

def iterate(n):
    global T
    temp = [0 for i in xrange(N)]
    for i in xrange(N):
        temp[i] = E[i]*(alpha[i]*dot(W, T[n-1], i) + beta[i])
        temp[i] = round(temp[i], 2)
        if temp[i] < 0:
            temp[i] = 0.0
    T[n] = temp

#W = setW()
for n in xrange(1,50):
    iterate(n)
print T
