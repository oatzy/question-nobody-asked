#string = "e?ua?i??"
string = "?a?"
guesses = ["e","i","o","u"]
#guesses = []
length = len(string)
count = 0

dictionary = open('enable2k.txt', 'r')

for word in dictionary:
    check = 1
    word = word.strip("\n")
    if len(word) == length:
        for letter in range(length):
            if string[letter] != "?":
                check = check * (word[letter] == string[letter])
                check = check * (word.count(string[letter]) == string.count(string[letter]))
        for G in range(len(guesses)):
            check = check * (guesses[G] not in word)
    else:
        check = 0
    if check == 1:
        count += 1
        print word
print count

dictionary.close()
