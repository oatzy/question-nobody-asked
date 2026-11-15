import random as r

string = "If you have ever taken the time to read some spam and you really should you might have come across something like this text that almost seems human but just doesn't quite make sense. here is a famous sentence that has a similar effect has anyone really been far as decided to use even go want to do look more like? there are several theories as to what is going on there. but while no-one is entirely sure what is going on some have postulated that it like the top quote and some spam was text generated with Markov Chains."
ss = string.split()

roots = []
stems = []

def chop():
    for i in xrange(len(ss)-1):
        if ss[i] not in roots:
            roots.append(ss[i])
            stems.append([ss[i+1]])
        else:
            stems[roots.index(ss[i])] += [ss[i+1]]

def generate():
    length = 140 #length of output string, measured char-wise
    temp = ''
    word = r.choice(roots)
    temp = temp + word
    while len(temp) <= length:
        word = r.choice(stems[roots.index(word)])
        temp = temp + " " + word
    return temp

def out(): #output's the chopped text to a csv file for external use
    f = open('markov-out.csv', 'a')
    for i in xrange(len(roots)):
        temp = roots[i]
        for j in stems[i]:
            temp = temp+","+ j
        temp = temp +'\n'
        f.write(temp)
    f.close()

chop()
print generate()
