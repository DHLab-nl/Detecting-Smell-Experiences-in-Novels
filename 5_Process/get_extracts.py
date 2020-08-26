"""Retreive extracts wrt. previous lexicon update cycle. 

Update extracts.json and output cycle extracts as extracts-{cycle}.txt for easy inspection

Example
    $ python3 get_extracts.py 4 working_folder
    $ python3 get_extracts.py 4 _aroma_NOUN+ADJ

Args:
    n (int): number of (CPU Threads) processes to use
    working_folder: 

Required in working folder:
    extracts.json: {"cycle":[([seeds], extract, parsed_extract),..],..}
    lexicon.json:   [
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
required in datasets:
    harvesting.json: {"book_code": [sentence, parsed sentence tuples],.. }
"""

import json
import multiprocessing
import os
import re
import sys

import regex
from tqdm import tqdm
# add libraries to path
sys.path.append(os.path.join(sys.path[0], "libraries"))
# add working folder to path
sys.path.append(os.path.join(sys.path[0], sys.argv[2]))

from CHUNKS import chunks
from pattern_abstraction import convert_patterns, expand_chunks, to_chunks
from PATTERNS import extraction_patterns, identification_patterns


def main(argv):

    # CL arguments
    folder = argv[1]
    n = int(argv[0])

    # get a list of previously seen extracts, from all prior cycles
    extracts_file = folder + "/extracts.json"
    previous_extracts, current_cycle = get_extracts(extracts_file)
    # previous_extracts = {"cycle":[([seeds], extract, parsed_extract),..],..}

    print(f"current cycle = {current_cycle}")

    seen_extracts = extracts_as_set(previous_extracts)
    # seen_extracts = {set of unparsed extracts previously seen}

    # Collect the previous cycle's lexicon entries
    with open(folder + "/lexicon.json", "r") as f:
        lexicon = json.load(f)
    vocabulary = get_lexicon(lexicon)  # [(compiled re, (coincident phrases),..]
    # [(compiled re, (coincident phrases),..]

    # compile previously seen abstractions
    seen_abstractions = identification_patterns
    seen_patterns = compile_patterns(seen_abstractions)

    # ITERATE THROUGH HARVESTING SET, extracting where
    #   * an extract is unseen
    #   * and where known patterns do not match

    with open("./datasets/harvesting.json", "r") as f:
        dataset = json.load(f)
    # dataset = {"book_code": [(sentence, parsed sentence),..]}

    # iterate through the harvesting set
    for book_index, (book_code, extracts) in enumerate(tqdm(dataset.items())):

        # discard extracts already seen
        extracts_trimmed = trim_extracts(extracts, seen_extracts)  # [(extract, parsed_extract),...]

        # split extracts n chunks, for multi-proccessing
        extract_sets = group_extracts(extracts_trimmed, n)  # [[(extract, parsed_extract),...],...]

        processes = []
        queue = multiprocessing.Queue()
        # iterate through the extract chunks as separate processes
        for i in range(n):

            # run vocabulary pattern matching against trimmed extracts
            process = multiprocessing.Process(
                target=mapped_function, args=(extract_sets[i], vocabulary, seen_patterns, queue,),
            )
            process.start()
            processes.append(process)

        # collect process output
        for r in range(n):
            previous_extracts[current_cycle] += queue.get()

        # terminate the processes
        for process in processes:
            process.join()

        # save to json
        with open(folder + "/extracts.json", "w") as f:
            json.dump(previous_extracts, f, ensure_ascii=False)

        # save ouput to text files for inspection
        with open(folder + f"/extracts-{current_cycle}.txt", "w") as f:
            for phrases, extract, parsed_extract in previous_extracts[current_cycle]:
                f.write("\n\n")
                f.write(f"{phrases}")
                f.write("\n" + extract)
                f.write("\n" + parsed_extract)


def mapped_function(extract_set, vocabulary, seen_patterns, queue):
    """Iterate through the extract_set and return a list of those extracts matching the previous lexicon cycle entries.
    """

    returned = []

    for extract, parsed_extract in extract_set:

        for v_pattern, phrases in vocabulary:
            mo_lexicon = regex.search(v_pattern, parsed_extract)

            if mo_lexicon:
                # check does not conform to a seen pattern
                mo_seen = None
                for seen_abstraction, seen_compiled in seen_patterns:
                    mo_seen = regex.match(seen_compiled, parsed_extract)
                    if mo_seen:
                        print("\n\nseen pattern")
                        print(extract)
                        print(seen_abstraction) 
                        break  # break seen pattern loop

            if mo_lexicon and not mo_seen:
                # if both vocab match and not conforming to seen_patterns
                returned.append((phrases, extract, parsed_extract))
                # print("\n\naccepted")
                # print(extract) 

    queue.put(returned)

def get_extracts(file):
    """Return existing extracts file container or create new.
    """

    # if file exists, then load
    if os.path.exists(file):
        with open(file, "r") as f:
            previous_extracts = json.load(f)
        # save as "folder/extracts.json" in case wish to revert
        with open(file, "w") as f:
            json.dump(previous_extracts, f, ensure_ascii=False, indent=4)
        # add new cycle
        previous_extracts[str(len(previous_extracts.keys()))] = []
    # if file doesn't exist, create new
    else:
        previous_extracts = {"0": []}

    # get the current cycle's index key for extracts
    current_cycle = str(list(previous_extracts.keys())[-1])

    return previous_extracts, current_cycle


def extracts_as_set(extracts):
    """Return the extracts to date as a set
    Args:
        extracts (dict): {"cycle":[([seeds], extract, parsed_extract),..],..}

    Return:
        set of seen extracts
    """

    seen_extracts = []

    for keys, values in extracts.items():
        for phrase, extract, parsed_extract in values:
            seen_extracts.append(extract)
    seen_extracts = set(seen_extracts)

    return seen_extracts

def get_lexicon(lexicon):
    """Return preivious lexicon vocab as a list of (compiled re, (coincident phrases)).
    Args:
        lexicon.json:   [
                            # cycle 0
                            [

                                # list of entries, each entry corresponds to pattern
                                [
                                    [(phrase0, phrase1), ..],  # list of coincidents phrases matched (e.g., adj, noun collection)
                                    pattern_A
                                ],
                                [
                                    [(phrase0, phrase1), ..],
                                    pattern_B
                                ]
                                ....
                            ],
                            ....
                        ]
"""
    patterns = []
    for entry in lexicon[-1]:  # each entry in previous cycle
        for phrases in entry[0]:
            try:
                converted_compounded_phrases = ""
                for phrase in phrases:
                    converted_compounded_phrases += ".*" + convert_patterns([phrase],chunks)[0]

                patterns.append((regex.compile(converted_compounded_phrases), phrases))
            except:
                print(f"lexicon error, please correct, token: {phrases}")

    return patterns


def compile_patterns(abstractions):
    """Assemble list of (abstracted_pattern, compiled) tuples of abstracted patterns.

    Args:
        abstractions: []
    Returns:
        [(abstracted_pattern, compiled),...]
    """
    # assemble (new) extraction patterns in python re format
    patterns = []  # patterns = [(abstraction, compiled pattern), ..]
    for abstraction in abstractions:
        print(abstraction)
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


def trim_extracts(extracts, seen_extracts):
    """Return a list of (extract, parsed_extract) for unseen extracts, not conforming to a known pattern.
    Args:
        extracts (list): [(sentence, parsed sentence),..]
    """
    # trim extract set, based on seen extracts
    extracts_trimmed = []
    for extract, parsed_extract in extracts:
        if extract not in seen_extracts:
            extracts_trimmed.append((extract, parsed_extract))


    return extracts_trimmed

def group_extracts(extracts, n):
    """Return extracts as a list of n lists of extracts (for multiprocessing)
       e.g., where n = 4, [[(extract, parsed_extract),...],[],[],[]]

    Args:
        extracts: [(sentence, parsed sentence),..]
    """
    extract_sets = [[] for i in range(n)]
    for i in range(0, len(extracts), n):
        for j in range(0, n):
            try:
                extract_sets[j].append(extracts[i + j])
            except:
                pass

    return extract_sets


if __name__ == "__main__":
    main(sys.argv[1:])
