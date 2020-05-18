"""Get extracts wrt. wrt. previous lexicon update.
Example
    $ python3 get_extracts.py

requires in dir.:
    parsed_extracts.json: {book_code:[(seed, extract, parsed_extract),..],..}
"""

import json
import os
import re
import sys

import regex
from tqdm import tqdm

from CHUNKS import chunks
from pattern_abstraction import convert_patterns, expand_chunks, to_chunks
from PATTERNS import extraction_patterns


def main(argv):

    # set up writing to extracts.json as previous_extracts
    if os.path.exists("extracts.json"):
        with open("extracts.json", "r") as f:
            previous_extracts = json.load(f)
        previous_extracts[str(len(previous_extracts.keys()))] = []
    else:
        previous_extracts = {"0": []}
    current_key = list(previous_extracts.keys())[-1]

    # list of all previously seen extracts
    seen_extracts = []
    for keys, values in previous_extracts.items():
        for phrase, extract, parsed_extract in values:
            seen_extracts.append(extract)
    seen_extracts = set(seen_extracts)

    # import lexicon
    with open("lexicon.json", "r") as f:
        lexicon = json.load(f)

    # import harvesting set
    with open("harvesting.json", "r") as f:
        dataset = json.load(f)

    # add unseen extracts, which matching vocab of last lexicon round to ....
    for book_code, extracts in tqdm(dataset.items()):
        for extract, parsed_extract in tqdm(extracts):

            # ignore extracts already seen
            if extract not in seen_extracts:

                for cycle in lexicon[-1]:

                    for phrase in cycle[0]:

                        try:
                            # convert phrase (abstraction) to python pattern
                            pattern = convert_patterns([phrase], chunks)[0]

                            mo = regex.match("^.*" + pattern + ".*", parsed_extract)
                            if mo:
                                previous_extracts[current_key].append(
                                    (phrase, extract, parsed_extract)
                                )
                                break
                        except:
                            print(f"lexicon failure, token: {phrase}. AMEND")
                            exit(1)
            else:
                print("yah")

    # save to json
    with open("extracts.json", "w") as f:
        json.dump(previous_extracts, f, ensure_ascii=False)

    # save ouput to text files for inspection
    with open(f"extracts-{current_key}.txt", "w") as f:
        for phrase, extract, parsed_extract in previous_extracts[current_key]:
            f.write("\n\n")
            f.write(phrase)
            f.write("\n" + extract)
            f.write("\n" + parsed_extract)


if __name__ == "__main__":
    main(sys.argv[1:])
