from random import randint as r

#Global Variables
board = [0 for i in xrange(101)]
S = 0
moves = []
jumps = [[1,38],[4,14],[9,31],[16,6],[21,42],[28,84],[36,44],[47,26],[49,11],[51,67],[56,53],[62,19],[64,60],[71,91],[80,100],[87,24],[93,73],[95,75],[98,78]]


#Funtions

#standard game
def play(S,moves):
    M = 0
    while S < 100:
        S += r(1,6)
        if S>100:
            S = 100
        board[S] += 1
        for i in jumps:
            if i[0] == S:
                S = i[1]
                board[S] += 1
        M += 1
    moves += [M]

#loopback end
def playL(S,moves):
    M = 0
    while S != 100:
        S += r(1,6)
        if S>100:
            S = 200-S
        board[S] += 1
        for i in jumps:
            if i[0] == S:
                S = i[1]
                board[S] += 1
        M += 1
    moves += [M]

#triple sixes
def playAlt(S,moves):
    M = 0
    m = 0
    c = 0
    while S != 100:
        m = r(1,6)
        if m == 6:
            c += 1
        else:
            c = 0
        if c == 3:
            S = 0
        elif S + m > 100:
            S = 100
        else:
            S += m
        board[S] += 1
        for i in jumps:
            if i[0] == S:
                S = i[1]
                board[S] += 1
        M += 1
    moves += [M]

#counts how often you land on snakes and ladders
def SnL(board):
    s = 0
    l = 0
    for i in jumps:
        if i[0] > i[1]:
            s += board[i[0]]
        else:
            l += board[i[0]]
    return [s,l]


#Main Loop
for i in xrange(10000):
    S = 0
    playAlt(S,moves)
print board
