import math

#birth & death rates; set to 0 for simplest model
b = 1.5
d = 0.0012 #proportional death rate

D = 1.4 #alternate, constant death rate

#Other variables
f = 0.001 #follow rate
m = 0.0002 #followers' effect rate; should be inv prop to N[0]
u = 0.0009 #unfollow rate
r = 0.00009 #refollow rate
i = 1024 #iterations

#Initial conditions
S = [1000] #initial population size
I = [1] #should => 1
R = [0] #typically 0
N = [S[0]+I[0]+R[0]] #total population  size


def main(S,I,R): #with proportional death rate
    for n in xrange(0,i):
        S += [(1-f-d)*S[n]+b-(m*math.log(S[n])*I[n])]
        I += [r*R[n]+(1-u-d)*I[n]+f*S[n]+(m*math.log(S[n])*I[n])]
        R += [u*I[n]+(1-r-d)*R[n]]
        

def main1(S,I,R,N): #with alternate death rate
    for n in xrange(0,i):
        S += [(1-f-(D/N[n]))*S[n]+b-(m*math.log(S[n])*I[n])]
        I += [r*R[n]+(1-u-(D/N[n]))*I[n]+f*S[n]+(m*math.log(S[n])*I[n])]
        R += [u*I[n]+(1-r-(D/N[n]))*R[n]]
        N += [S[n+1]+I[n+1]+R[n+1]]


main(S,I,R) #run main
#main1(S,I,R,N)

#integerize I
I1 = []
for i in I:
    I1+= [int(round(i))]
print I1
