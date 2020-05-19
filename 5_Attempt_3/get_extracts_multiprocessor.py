"""Get extracts wrt. wrt. previous lexicon update.
Example
    $ python3 get_extracts.py 4

Args:
    n (int): number of (CPU Threads) processes to use

requires in dir.:
    parsed_extracts.json: {"cycle":[(seed, extract, parsed_extract),..],..}
    harvesting.json: {"book_code": [list of sentence, parsed sentence tuples],.. }
    lexicon.json:   [
                        # phrases from patterns 0 (i.e. cycle 0)
                        [

                            [
                                [list of parsed (match object) phrases],
                                abstracted lexico-syntactic pattern,
                            ],
                            ...
                        ],

                        # phrases from pattern 1, etc
                    ]
"""

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


def main(argv):

    # set up number of CPUs to use
    if any(argv):
        number_of_processes = int(argv[0])
    else:
        number_of_processes = 1

    # read in previously collected extracts, or if non-existing create new container
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

    # compile lexicon as regex patterns
    patterns = []
    for cycle in lexicon[-1]:
        for phrase in cycle[0]:
            try:
                patterns.append((regex.compile(convert_patterns([phrase], chunks)[0]), phrase))
            except:
                print(f"lexicon error, token: {phrase}")

    # import harvesting set
    with open("harvesting.json", "r") as f:
        dataset = json.load(f)

    # add unseen extracts, which matching vocab of last lexicon round to ....
    for book_index, (book_code, extracts) in enumerate(tqdm(dataset.items())):

        # discard extracts already seen
        extracts_trimmed = []
        for extract, parsed_extract in extracts:
            if extract not in seen_extracts:
                extracts_trimmed.append((extract, parsed_extract))

        # split extracts in n chunks, where n is ....
        extract_sets = [[] for i in range(number_of_processes)]
        for i in range(0, len(extracts_trimmed), number_of_processes):
            for j in range(0, number_of_processes):
                try:
                    extract_sets[j].append(extracts_trimmed[i + j])
                except:
                    pass

        # iterate through the extract chunks as separate processes
        processes = []
        queue = multiprocessing.Queue()

        for i in range(number_of_processes):

            process = multiprocessing.Process(
                target=mapped_function, args=(extract_sets[i], patterns, queue,),
            )
            process.start()
            processes.append(process)

        # collect process output
        for r in range(number_of_processes):
            previous_extracts[current_key] += queue.get()

        # terminate the processes
        for process in processes:
            process.join()

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


def mapped_function(extract_set, patterns, queue):
    """Iterate through the extract_set and return a list of extracts with the last lexicon cycles entries present.
    """
    # ignore extracts already seen

    returned = []
    for extract, parsed_extract in extract_set:
        for pattern, phrase in patterns:
            mo = regex.search(pattern, parsed_extract)
            if mo:
                returned.append((phrase, extract, parsed_extract))
                break

    queue.put(returned)


if __name__ == "__main__":
    main(sys.argv[1:])
