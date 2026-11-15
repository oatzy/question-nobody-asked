from math import log

alphabet = "abcdefghijklmnopqrstuvwxyz"
#scores = [1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10] #Scrabble scores
scores = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]
Score = 0

#GuessSet = ["e", "t", "a", "o", "i", "n" ,"s"] # Most common letters
GuessSet = ["a", "e", "i", "o", "u"] # Alternative, vowel guess-set

#String = "equality"
String = "jazz"
length = len(String)

WGuesses = []
GuessString = String


def Scorer(string):
    total = 0
    for i in range(26):
        if alphabet[i] in string:
            total += scores[i]
    return total

def Guesser(string):
    global WGuesses
    global GuessString
    for i in range(length):
        if String[i] not in GuessSet:
            GuessString = GuessString.replace(String[i], "?")
    for i in GuessSet:
        if i not in String:
            WGuesses += [i]

def CountPossibles(string):
    
    dictionary = open('enable2k.txt', 'r')

    count = 0
    for word in dictionary:
        check = 1
        word = word.strip("\n")
        if len(word) == length:
            for letter in range(length):
                if string[letter] != "?":
                    check = check * (word[letter] == string[letter])
                    check = check * (word.count(string[letter]) == string.count(string[letter]))
            for G in range(len(WGuesses)):
                check = check * (WGuesses[G] not in word)
        else:
            check = 0
        if check == 1:
            count += 1

    dictionary.close()

    return count

def LetterEntropy():
    n = 0
    H = 0
    for i in range(26):
        if alphabet[i] not in GuessSet:
            H += (scores[i]/100.0)*log(100.0/scores[i], 2)
    for i in range(length):
        if (String.index(String[i]) == i) and (GuessString[i] == "?"):
            n += 1
    return n*H

print "                       {}\n".format(String)
Score += Scorer(String)
Score = 1-(Score/100.0)
print "Uncertainty:           {}".format(Score)
Guesser(String)
print "Guess String:          {}".format(GuessString)
print "Incorrect Guesses:     {}".format(WGuesses)
Count = CountPossibles(GuessString)
print "Possible Word Matches: {}".format(Count)
print "Letter Entropy:        {}".format(LetterEntropy())

Score = (min(LetterEntropy(), log(Count, 2))+1)*Score
print "Score:                 {}".format(Score)

""" Note on Guess-Sets - which you chose will affect the score.
    With the word 'equality', you get 1 result for the common letters set
    3 results for the vowels set.

    I would probably advise the vowels set, since most people
    start by guessing vowels. """
