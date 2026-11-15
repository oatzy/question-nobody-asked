# Variables
f = 0.001 #follow rate
u = 0.0001 #unfollow rate
r = 0.00005 #refollow rate
i = 1024 #iterations

#Initial conditions
S = [1000] #typically initial population size
I = [0] #typically 0
R = [0] #typically 0


def main(S,I,R): #simplest model
    for n in xrange(0,i):
        S += [(1-f)*S[n]]
        I += [r*R[n]+(1-u)*I[n]+f*S[n]]
        R += [u*I[n]+(1-r)*R[n]]


main(S,I,R) #run main

#integerize I
I1 = []
for i in I:
    I1+= [int(round(i))]
print I1
