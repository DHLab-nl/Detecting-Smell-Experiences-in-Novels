"""
amend _text__DET to _text_DET* 
"""
from pattern_abstraction import convert_patterns
import regex
import json


def main():

    with open("lexicon.json", "r") as f:
        lexicon = json.load(f)

    lexicon_new = []
    for cycle_index, cycle in enumerate(lexicon):
        lexicon_new.append([])
        for set_index, set in enumerate(cycle):
            lexicon_new[cycle_index].append([[]])

            # iterate through each phrase and perform replacements
            for phrase in set[0]:

                new_phrase = regex.sub(r"_DET ", "_DET* ", phrase)
                lexicon_new[cycle_index][set_index][0].append(new_phrase)

            if len(set) > 1:
                abstraction = lexicon[cycle_index][set_index][1]
                lexicon_new[cycle_index][set_index].append(abstraction)

    with open("lexicon.json", "w") as f:
        json.dump(lexicon_new, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
