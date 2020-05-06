"""
Example:
    $ python3 identify_sequences.py parsed_extracts.json
"""


import spacy
from difflib import SequenceMatcher
import re
import sys
import json


def get_match(sentence1, sentence2):
    """Return sequential token matches and a similarity score.

    Args:
        sentence1 (string):
        sentence2 (string):
    """
    sm = SequenceMatcher(None, sentence1, sentence2)

    sequential_matches = []
    for blocks in sm.get_matching_blocks():

        a = blocks[0]
        l = blocks[2]
        sequence_match = sentence1[a:a+l]

        # iterate over tokens in sequence_match
        for token in sequence_match.split():
            # include only complete token space separated
            if token in set(sentence1.split(" ")):
                sequential_matches.append(token)
            else:
                pass

    sentence = " ".join([token.strip() for token in sequential_matches])

    return sentence  # , sm.ratio()


def identify_matches(extracts):

    commonalities = []

    # iterate over extracts and find patterns for all combinations
    for extract_index, extract1 in enumerate(extracts):
        for extract2 in extracts[extract_index+1:]:
            commonalities.append(get_match(extract1, extract2))

    return list(set(commonalities))


def main(argv):

    # open parsed text
    with open(argv[0], "r") as f:
        extracts = json.load(f)

    # output matches set
    with open("commonalities.txt", "a") as f:
        for pattern in identify_matches(extracts):
            f.write(pattern + "\n\n")

if __name__ == "__main__":
    main(sys.argv[1:])
