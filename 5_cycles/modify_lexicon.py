"""Make lexicon substitutions, by specified working folder.

Used to convert __DET into __DET*

Example:
    $python3 modify_lexicon.py working_folder

Args:
    working_folder (string):

Required in working folder:

    lexicon.json:   [
                        # cycle 0
                        [

                            [
                                [(phrase0, phrase1 from extract0,..), ..],
                                pattern0_A
                            ],
                            [
                                [(phrase0, phrase1 from extract0,..), ..],
                                pattern0_B
                            ]
                            ....
                        ],
                        ....
                    ]

Returns:

"""
import regex
import json
import sys
import os

sys.path.append(os.path.join(sys.path[0], "libraries"))
sys.path.append(os.path.join(sys.path[0], sys.argv[1]))
from pattern_abstraction import convert_patterns

substitutions = {
        "_aroma_NOUN+VERB": [("_DET ", "_DET* ")],
        "_aroma_NOUN+ADJ": [("_DET ", "_DET* ")],
}

def main(argv):

    # open the lexicon
    folder = argv[0]
    with open(folder + "/lexicon.json", "r") as f:
        lexicon = json.load(f)

    print(lexicon)

    # create a new lexicon, with 
    lexicon_new = []
    for cycle_index, cycle in enumerate(lexicon):
        lexicon_new.append([])
        for entry_index, entry in enumerate(cycle):
            lexicon_new[-1].append([[]])

            # iterate through phrases and perform replacements
            for phrases in entry[0]:
                new_phrases = []
                for phrase in phrases:

                    # perform all substitutions
                    new_phrase = phrase
                    for sub1, sub2 in substitutions[folder]:
                        new_phrase = regex.sub(sub1, sub2, new_phrase)
                        new_phrases.append(new_phrase)

                lexicon_new[cycle_index][entry_index][0].append(new_phrases)

            # cases where associated pattern listed (i.e., not just seed words) - coopy over
            if len(entry) > 1:
                abstraction = lexicon[cycle_index][entry_index][1]
                lexicon_new[cycle_index][entry_index].append(abstraction)

    with open(folder + "/lexicon.json", "w") as f:
        json.dump(lexicon_new, f, ensure_ascii=False, indent=4)

    # save copy of old lexicon
    with open(folder + f"/lexicon_cycle_{cycle_index}_unmodified.json", "w") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
