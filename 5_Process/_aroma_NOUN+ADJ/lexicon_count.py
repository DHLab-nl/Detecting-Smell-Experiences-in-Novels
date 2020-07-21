"""small script to count the lexicon entries by cycle
"""
import json

with open("lexicon.json") as f:
    lexicon = json.load(f)

mini = {}
for i, cycle in enumerate(lexicon):
    mini[str(i)] = 0 
    for entry in cycle:  # each entry corresponds to a pattern
        mini[str(i)] += len(entry[0])

print(mini)





