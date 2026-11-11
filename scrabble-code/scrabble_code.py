"""
Assuming a 4 digit code which is derived from a 4 letter word
as scored in Scrabble, how many valid codes are there?
"""
from collections import Counter

WORDS = "/usr/share/dict/words"

SCORES = {}
SCORES.update({c: '1' for c in "EAIONRTLSU"})
SCORES.update({c: '2' for c in "DG"})
SCORES.update({c: '3' for c in "BCMP"})
SCORES.update({c: '4' for c in "FHVWY"})
SCORES.update({c: '5' for c in "K"})
SCORES.update({c: '8' for c in "JX"})

codes = Counter()

with open(WORDS) as f:
    for word in f:
        word = [c.upper() for c in word if c.isalpha()]
        if len(word) != 4 or "Q" in word or "Z" in word:
            continue
        try:
            code = "".join(SCORES[c] for c in word)
        except KeyError:
            continue  # accented
        codes.update([code])

print(f"Total: {len(list(codes.elements()))}")
print(f"Unique: {len(codes)}")
print(f"Most common: {codes.most_common(5)}")
