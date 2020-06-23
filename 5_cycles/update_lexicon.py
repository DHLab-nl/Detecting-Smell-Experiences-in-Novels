"""Iterate through /datasets/harvesting.json, and for identified patterns, extract match objects, and save to lexicon.json.

Notes:
    * only new (coincident) match object not already present in the lexicon
    * implemented as a multi-processor (pattern matching is slow and processor heavy) - user can select number of cores to use

Example
    $ python3 update_lexicon_multiprocess.py n working_directory 
    $ python3 update_lexicon_multiprocess.py 4 _aroma_NOUN

Args:
    n (int): number of cores to utilize in multicore processing
    working_directory: sub directory wrt. current cycles

Requires in working directory:
    folder/PATTERNS.py
    folder/lexicon.json:
                    [
                        # cycle 0
                        [
                            # entry 0 in cycle: all coincident extracts corresponding to a pattern
                            (
                                [("_sharp_ADJ", "_lemon_NOUN"), ... ],  #list of coincident vocabulary tuples tagetted by pattern A
                                pattern_A,
                            ),
                            ....
                        ],
                        ....
                    ]

Note: lexicon.json seeding, [[[[["_sharp_ADJ", "_lemon_NOUN"], ["_awful_ADJ", "_bile_ADJ"]]]]] will seed against each set of coincident words

Requires in /libraries:
    datasets/harvesting.json: {"book_code": [list of sentence, parsed sentence tuples],.. }

"""

import itertools
import json
import multiprocessing
import os
import re
import sys

import regex
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], "libraries"))
sys.path.append(os.path.join(sys.path[0], sys.argv[2]))

from CHUNKS import chunks
from pattern_abstraction import convert_patterns, expand_chunks, to_chunks
from PATTERNS import extraction_patterns
from nltk.tokenize import word_tokenize






def main(argv):

    # SET PARAMETERS

    n = int(argv[0])
    folder = argv[1]

    # IMPORT FROM FILES
    # harvesting set, lexicon

    # import harvesting dataset
    with open("datasets/harvesting.json", "r") as f:
        harvesting_set = json.load(f)

    # import lexicon: MUST exist to seed process.
    with open(folder + "/lexicon.json", "r") as f:
        lexicon = json.load(f)

    # ASSEMBLE FROM LEXICON
    # assemble: previous lexicon vocab, pattern abstractions recorded in lexicon,

    # complete list of lexicon vocab tuples : [["sharp", "apple blossom"],...]
    previous_vocab = __previous_vocabulary(lexicon)

    # previous previous abstracted patterns seen by lexicon
    previous_abstractions = []  # [abstracted_pattern1, abstracted_pattern2,...]
    for cycle in lexicon:
        for entry in cycle:
            if len(entry) > 1:
                previous_abstractions += entry[1]

    # new lexicon round @ lexicon[-1]
    lexicon.append([])

    # ASSEMBLE compiled unseen patterns from PATTERNS.py

    # assemble (unseen patterns)
    patterns = __compile_new_patterns(previous_abstractions, extraction_patterns)

    # assemble the patterns in to blocks of n patterns for multiprocessing
    pattern_sets = __group_patterns(patterns, n)

    # ITERATE OVER HARVESTING SET, RETREVE MATCHES FOR UNSEEN PATTERNS, store in results{}

    # store matches by pattern
    results = {}
    for abstraction, pattern in patterns:
        results[abstraction] = []

    print(f"Iterating over book extracts")
    for book_code, book_extracts in tqdm(harvesting_set.items()):

        for patterns in pattern_sets:

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
                # results[abstraction] = [[phrase in extract0, phraserin extract0], ...]

            # collect output from multiple threads
            for p in processes:
                p.join()

    # APPEND ONLY UNSEEN (as a group) COINCIDENT TARGETS TO LEXICON
    for abstraction, r in results.items():
        if any(r):
            new_r = list(set(r) - set(previous_vocab))  #list of phrases
            lexicon[-1].append([new_r, abstraction])


    # SAVE LEXICON
    with open(folder + "/lexicon.json", "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=4)


def __previous_vocabulary(lexicon):
    """Assemble a list of ALL previous lexicon vocabulary.

    Args: 
        lexicon :
                    [
                        # cycle 0
                        [
                            # entry 0 in cycle: all coincident extracts corresponding to a pattern A
                            (
                                [("sharp", "apple blossom"), ... ],  #list of coincident vocabulary tuples tageted by pattern A
                                pattern_A,
                            ),
                            ....
                        ],
                        ....
                    ]
    Returns:
        [(coincident phrases),...]
    """
    previous_vocab = []
    for cycle in lexicon:
        for entry in cycle:
            if len(entry) > 1:
                for r, abstraction in cycle:
                    for phrases in r:
                        previous_vocab.append(tuple(phrases))
            else:
                for phrases in entry[0]:
                    previous_vocab.append(tuple(phrases))

    return previous_vocab


def __compile_new_patterns(previous_abstractions, extraction_patterns):
    """Assemble (unseen by lexicon) patterns.

       i.e., compare previous_abstracted patterns [] recorded in lexicon, against
       the abstracted patterns in extraction_patterns [] in PATTERNS.py 

    Args:
        previous_abstractions: []
        extraction_patterns: []
    Returns:
        [(abstracted_pattern, compiled_pattern),...]

    Note: patterns are compiled for use with regex.match()
    """
    # assemble (new) extraction patterns in python re format
    patterns = []  # patterns = [(abstraction, compiled pattern), ..]
    for abstraction in extraction_patterns:
        print(abstraction)
        if abstraction not in previous_abstractions:  # COLLECT NEW PATTERNS ONLY
            patterns.append(
                (
                    abstraction,
                    regex.compile(
                        "^.*" + convert_patterns([abstraction], chunks)[0] + ".*",
                        re.MULTILINE,
                    ),
                )
            )

    return patterns


def expand_lexicon(book_extracts, pattern, queue):
    """return list of matches, for all extracts for given pattern
    """
    output = []
    for extract, parsed_extract in book_extracts:

        mo = regex.match(pattern, parsed_extract)

        # if a pattern match, add match object to lexicon
        if mo:
            if any(mo.groups()):
                matches = []
                for match in mo.groups():
                    # only add matches that are new to the lexicon
                    match = remove_dep(match)
                    matches.append(match)
                output.append(tuple(matches))  # explicitly cast, because tuples can be made sets
    queue.put(output)


def remove_dep(parsed_phrase):
    """Remove the dep portion from the parsed lexicon phrase.
    e.g., amod_open_ADJ nsubj_buds_NOUN, becomes, "_open_ADJ _buds_NOUN"
    """

    amended = "" 
    for token in word_tokenize(parsed_phrase):

        if regex.match("\S+_\S+_\S+", token):
            if len(amended) == 0:
                amended += "_" + "_".join(token.split("_")[1:])
            else:
                amended += " " + "_" + "_".join(token.split("_")[1:])


    return amended


def __group_patterns(patterns, n):
    """Return extracts as a list of n lists of extracts (for multiprocessing).

    Args:
        extracts: [(sentence, parsed sentence),..]
    Returns:
       [[(abstracted_pattern, compiled),...],...]
    """
    pattern_sets = [[] for i in range(n)]
    for i in range(0, len(patterns), n):
        for j in range(0, n):
            try:
                pattern_sets[j].append(patterns[i + j])
            except:
                pass

    return pattern_sets



if __name__ == "__main__":
    main(sys.argv[1:])
