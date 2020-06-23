"""return validation sets for each identification_pattern in PATTERNS.py, for unseen patterns (not in validated_patterns.json)
   if more than 10 extracts are returned for a pattern, 10 patterns are randomnly selected
   auto updates validated_patterns.json once complete

Example
    $ python3 validate.py n working_folder
    $ python3 validate.py 4 _aroma_NOUN

Args:
    n (int): number of (CPU Threads) processes to use
    working_folder

requires:
    ./datasets/validation.json: {"book_code": [list of sentence, parsed sentence tuples],.. }
    .{working_folder}/PATTERN.py
    """

import json
import multiprocessing
import os
import re
import sys

sys.path.append(os.path.join(sys.path[0], "libraries"))
sys.path.append(os.path.join(sys.path[0], sys.argv[2]))

import regex
from tqdm import tqdm
import random

from CHUNKS import chunks
from pattern_abstraction import convert_patterns, expand_chunks, to_chunks
from PATTERNS import identification_patterns


def main(argv):

    folder = argv[1]
    results = {}

    # set up number of CPUs to use
    if any(argv):
        n = int(argv[0])
    else:
        n = 1

    patterns = get_unvalidated_patterns(folder)

    # create sets of n (compiled pattern, pattern) tuples for multiprocessing
    pattern_sets = [[]]  # [[(compiled_pattern, abstractionl),...],...]
    for pattern in patterns:
        if len(pattern_sets) < n-1:
            pattern_sets[-1].append(pattern)
        else:
            pattern_sets.append([])
            pattern_sets[-1].append(pattern)

    # import validation set
    with open("./datasets/validation.json", "r") as f:
        dataset = json.load(f)

    # examine validation set for patterns, collect a dictionary of matching extract by pattern
    for book_index, (book_code, extracts) in enumerate(tqdm(dataset.items())):

        # iterate through the extract chunks as separate processes

        # iterate through set of n patterns
        for patterns in pattern_sets:

            processes = []
            queue = multiprocessing.Queue()

            # iterate through each pattern in-turn, get matching extracts
            for compiled_pattern, abstraction in patterns:

                process = multiprocessing.Process(
                    target=mapped_function,
                    args=(extracts, [(compiled_pattern, abstraction)], queue,),
                )
                process.start()
                processes.append(process)

            # merge the output dictionaries {abstraction: list of extracts} with
            for process in processes:
                q = queue.get()
                results = merge_dict(results, q)

            # terminate the processes
            for process in processes:
                process.join()

    # update validated_patterns.json
    with open(folder + "/validated_patterns.json", "w") as f:
        json.dump(list(results.keys()), f)

    # save new validation extracts
    save_to_json(folder, results)


def save_to_json(folder, results):
    """Save a random sample of max 100 extracts to json, by pattern.
       random sample without replacement.
    """
    for abstraction, extracts in results.items():

        with open(folder + f"/validation_{abstraction}.json", "w") as f:
            if len(extracts) > 10:
                extracts = random.sample(extracts, 10)
            json.dump(extracts, f, ensure_ascii=False, indent=4)


def get_unvalidated_patterns(folder):
    """Return a list of (compiled_converted_abstraction, abstraction) for each previously unvalidated pattern in pattern.py
    """

    # get previously validated abstractions
    if os.path.exists(folder + "/validated_patterns.json"):
        with open(folder + "/validated_patterns.json", "r") as f:
            validated_abstractions = json.load(f)
    else:
        validated_abstractions = []

    # identify and list unvalidated patterns present in identification_patterns
    unvalidated_abstractions = [
        pattern
        for pattern in identification_patterns
        if pattern not in validated_abstractions
    ]

    # create a list of (compiled_pattern, abstraction) tuples for unvalidated
    patterns = []
    for abstraction in unvalidated_abstractions:
        print(abstraction)
        patterns.append(
            (regex.compile(convert_patterns([abstraction], chunks)[0]), abstraction)
        )

    return patterns


def merge_dict(a, b):
    """
    a (dict): a{k: list of values,...}
    b (dict): b{k: list of values,...}

    """
    for k, v in b.items():
        if k in a:
            a[k] += v
        else:
            a[k] = v

    return a


def mapped_function(extract_set, patterns, queue):
    """Return a dictionary of abstractions, and a corresponding list of matching extracts

    Args:
        extract_set (list): [(extract, parsed_extract), ...]
        patterns (list): [(compiled_pattern, abstraction), ...]
        queue: multiprocessor.Queue object
    """
    # ignore extracts already seen

    returned = {}
    for extract, parsed_extract in extract_set:
        for compiled_pattern, abstraction in patterns:
            mo = regex.search(compiled_pattern, parsed_extract)
            if mo:
                if abstraction not in returned.keys():
                    returned[abstraction] = []
                returned[abstraction].append((extract, parsed_extract, "TP?"))

    queue.put(returned)


if __name__ == "__main__":
    main(sys.argv[1:])
