"""Get extracts from lexicon.
Example
    $ python3 get_extracts.py number

requires in dir.:
    parsed_extracts.json: {book_code:[(seed, extract, parsed_extract),..],..}
"""

import json
import re
import sys

import regex
from tqdm import tqdm

from CHUNKS import chunks
from PATTERNS import extraction_patterns
from pattern_abstraction import convert_patterns, expand_chunks, to_chunks 


def main(argv):

    # import lexicon
    with open("lexicon.json", "r") as f:
        lexicon = json.load(f)

    # import harvesting set
    with open("harvesting.json", "r") as f:
        dataset = json.load(f)

    output = []

    # iterate over extracts, check extracts for most recent set of lexicon words
    for book_code, extracts in tqdm(dataset.items()):
        for extract, parsed_extract in extracts:
            for lexicon_phrase in lexicon[-1]:

                # remove " ' from parsed extract
                parsed_extract = parsed_extract.replace('punct_"_PUNCT', "")
                parsed_extract = parsed_extract.replace("punct_'_PUNCT", "")

                # does the word match in the extract?
                pattern = convert_patterns([lexicon_phrase], chunks)[0]

                mo = regex.search(pattern, parsed_extract)
                if mo:
                    output.append((lexicon_phrase, extract))
                    break

    # save ouput
    if argv:
        x = argv[0]
    else:
        x = 0
    with open(f"extracts-{x}.txt", "w") as f:
        for lexicon_phrase, extract in output:
            f.write("\n\n")
            f.write(lexicon_phrase)
            f.write("\n"+extract)

if __name__ == "__main__":
    main(sys.argv[1:])
