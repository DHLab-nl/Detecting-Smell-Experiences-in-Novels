"""
    scapped! e.g. analysing the permutation of a single sentence with e.g. 20 words, each word considered as (dep, pos, text_pos) yield 3**20 or 2.5 billion combinations. this is insanely computationally intensive.
"""


import json
from collections import Counter

import numpy as np
from numpy.linalg import eig
from tqdm import tqdm


def list_combinations(list1, list2):
    """Create a new list of all possible permutations of 2 lists.
    
    Args:
        list1 (list): a list of strings
        list2 (list): a list of strings
    """
    output = []
    for item1 in list1:
        for item2 in list2:
            output.append(item1 + " " + item2)

    return output


def map_consecutive(sentence, previous=None):
    """Assemble all possible ngrams in a sentence.

    Args:
        sentence (list): a list of (dep, pos, token_pos) tuples corresponding
        to a sentence
    """
    print(previous)
    if len(sentence) > 1:
        if previous:
            previous = list_combinations(previous, sentence[0])
            return map_consecutive(sentence[1:], previous)
        else:
            previous = sentence[0]
            return map_consecutive(sentence[1:], previous)
    else:
        return list_combinations(previous, sentence[0])


def main():

    # import text extracts
    with open("extracts.json", "r") as f:
        extracts = json.load(f)

    combinations = []
    for book_code, book_extracts in extracts.items():
        print(f"mapping token combinations for book {book_code}")
        for sentence in tqdm(book_extracts):
            combinations += map_consecutive(sentence)


if __name__ == "__main__":
    main()
