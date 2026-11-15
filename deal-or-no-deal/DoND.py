from random import randint

wins = 0

def play(n):
    global wins
    smax = -1
    dmax = -1
    stick = -1
    for i in xrange(n):
        r = randint(1,13)
        if r > smax:
            smax = r
    dmax = smax
    for i in xrange(7-n):
        r = randint(1,13)
        if r > dmax:
            dmax = r
        if r > smax and stick < 0:
            stick = r
    if stick < 0:
        stick = randint(1, 13)
    if stick >= dmax:
        wins += 1

for j in xrange(8):
    wins = 0
    for i in xrange(10000):
        play(j)
    print wins

