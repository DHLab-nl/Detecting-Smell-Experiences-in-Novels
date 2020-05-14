"""Iterate through harvesting set, and for identified patterns, extract match objects as save to lexicon.json.

Notes:
    * only new match object entries added to lexicon.json

Example
    $ python3 get_lexicon.py

Requires in directory:
    parsed_extracts.json
"""

import json
import re
import sys
import os
import itertools

import regex
from tqdm import tqdm

from CHUNKS import chunks
from pattern_abstraction import convert_patterns, expand_chunks, to_chunks
from PATTERNS import extraction_patterns


def main():

    # import harvesting dataset
    with open("harvesting.json", "r") as f:
        harvesting_set = json.load(f)

    # import lexicon or create new
    if os.path.exists("lexicon.json"):
        with open("lexicon.json", "r") as f:
            lexicon = json.load(f)
    else:
        lexicon = []

    # new lexicon assembly round @ lexicon[-1]
    lexicon.append([])

    # assemble extraction patterns in python re format
    patterns = []
    for pattern in extraction_patterns:
        patterns.append(convert_patterns([pattern], chunks)[0])

    # iterate over book extracts
    print(f"Iterating over book extracts")
    for extract_index, (book_code, book_extracts) in enumerate(
        tqdm(harvesting_set.items())
    ):

        for extract, parsed_extract in book_extracts:

            # remove " and ' from sentences
            parsed_extract = parsed_extract.replace('punct_"_PUNCT', "")
            parsed_extract = parsed_extract.replace("punct_'_PUNCT", "")

            # group extracts under existing patterns, or group under unmatched
            for pattern in patterns:
                mo = regex.search(pattern, parsed_extract)

                # if a pattern match, add match object to lexicon
                if mo:
                    if any(mo.groups()):
                        for match in mo.groups():
                            # only add matches that are new to the lexicon
                            match = remove_dep(match)
                            if match not in list(itertools.chain(*lexicon)):
                                lexicon[-1].append(match)


    # save lexicon
    with open("lexicon.json", "w", encoding="utf-8") as f:
        json.dump(lexicon, f)


def remove_dep(parsed_extract):
    """Remove the dep from each token form extract string.
    e.g., amod_open_ADJ nsubj_buds_NOUN, becomes, "_open_ADJ _buds_NOUN"
    """

    amended = ""
    for token in re.split("\s+", parsed_extract):

        if len(amended) == 0:
            amended += "_" + "_".join(token.split("_")[1:])
        else:
            amended += " _" + "_".join(token.split("_")[1:])

    return amended

if __name__ == "__main__":
    main()
