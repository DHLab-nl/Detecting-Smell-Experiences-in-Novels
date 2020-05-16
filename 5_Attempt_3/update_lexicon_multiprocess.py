"""Iterate through harvesting.json, and for identified patterns, extract match objects as save to lexicon.json.

Notes:
    * only new match object entries added to lexicon.json
    * implemented as a multi-processor, a new process spawned for each pattern

Example
    $ python3 update_lexicon_multiprocess.py

Requires in directory:
    harvesting.json
    lexicon.json
"""

import itertools
import json
import multiprocessing
import os
import re
import sys

import regex
from tqdm import tqdm

from CHUNKS import chunks
from pattern_abstraction import convert_patterns, expand_chunks, to_chunks
from PATTERNS import extraction_patterns

book_extracts = []


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

    # get a list of previous vocabulary (from entire lexicon)
    previous_vocab = []
    for cycle in lexicon:
        for entry in cycle:
            if len(entry) > 1:
                for r, abstraction in cycle:
                    previous_vocab += r

    # get a list of previous patterns used, for extraction
    previous_abstractions = []
    for cycle in lexicon:
        for entry in cycle:
            if len(entry) > 1:
                previous_abstractions += entry[1]

    # new lexicon round @ lexicon[-1]
    lexicon.append([])

    # assemble (new) extraction patterns in python re format
    patterns = []  # patterns = [(abstraction, compiled pattern), ..]
    for abstraction in extraction_patterns:
        if abstraction not in previous_abstractions:  # collect new only
            patterns.append(
                (
                    abstraction,
                    regex.compile(
                        "^.*" + convert_patterns([abstraction], chunks)[0] + ".*",
                        re.MULTILINE,
                    ),
                )
            )

    # container to store match objects, by pattern
    results = {}
    for abstraction, pattern in patterns:
        results[abstraction] = []

    # iterate over book extracts
    print(f"Iterating over book extracts")
    for book_code, book_extracts in tqdm(harvesting_set.items()):

        # start the processes
        processes = []  # to store processes

        # to collect output from processes
        queue = multiprocessing.Queue()

        for abstraction, pattern in patterns:

            p = multiprocessing.Process(
                target=expand_lexicon, args=(book_extracts, pattern, queue),
            )
            p.start()
            processes.append(p)

        for abstraction, pattern in patterns:
            results[abstraction] += queue.get()

        # collect output from multiple threads
        for p in processes:
            p.join()

    # sift through results, and append only new
    for abstraction, r in results.items():
        new_r = list(set(r) - set(previous_vocab))
        lexicon[-1].append([new_r, abstraction])

    # save lexicon
    with open("lexicon.json", "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False)


def expand_lexicon(book_extracts, pattern, queue):
    """return list of matches
    """
    output = []
    for extract, parsed_extract in book_extracts:

        mo = regex.match(pattern, parsed_extract)

        # if a pattern match, add match object to lexicon
        if mo:
            if any(mo.groups()):
                for match in mo.groups():
                    # only add matches that are new to the lexicon
                    match = remove_dep(match)
                    output.append(match)
    queue.put(output)


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
