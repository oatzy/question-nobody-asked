import random
import numpy as np


#globals

pi = [0, 0.33, 0.27, 0.2, 0.13, 0.07]
ni = [0, 10, 10, 10, 10, 10]


#functions

def pick():
    p = pi[0];
    r = random.random();
    i = 0
    while (r > p):
        i += 1;
        p += pi[i]
    return i

def chomp(i):
    if ni[i] > 0:
        ni[i] -= 1

def run():
    while sum(ni) > 0:
        print sum(ni)
        c = np.random.poisson(1)
        for j in xrange(c):
            i = pick()
            chomp(i)

def run_simple():
    while sum(ni) > 0:
        print sum(ni)
        i = pick()
        chomp(i)

        
#main
        
if __name__ == "__main__":
    run()
