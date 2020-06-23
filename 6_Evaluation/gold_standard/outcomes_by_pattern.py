"""return a list of TN, TP, FP, FN outcomes for each extract by pattern

Example:
    $python3 outcomes_by_pattern.py n working_folder
    $python3 outcomes_by_pattern.py n _aroma_NOUN+VERB

"""
import json
import multiprocessing
import os
import re
import sys

import numpy as np
import regex
import spacy
# add libraries to path
sys.path.append(os.path.join(sys.path[0], "libraries"))
# add working folder to path
sys.path.append(os.path.join(sys.path[0], sys.argv[2]))

from CHUNKS import chunks
from pattern_abstraction import convert_patterns
from PATTERNS import identification_patterns


def evaluate(compiled_pattern, text, tags, nlp):
    """
    """
    # PARSE WITH SPACY
    text_parsed = ""
    doc = nlp(re.sub(r"\s+", " ", text.lower().replace("\n", " ")))
    for token in doc:
        text_parsed += f"{token.dep_}_{token.text}_{token.pos_} "

    # CHECK IF PATTERN MATCH, comparing against tags...TP or FP or ...
    mo = regex.search(compiled_pattern, text_parsed)
    if mo:  # pattern predicts IS  a smell experience
        if "d" in tags or "o" in tags:
            return "TP"  # annotator  POS
        else:
            return "FP"  # annotator NEG
    if not mo:  # pattern predicts NOT a smell experience
        if "d" in tags or "o" in tags:
            return "FN"  # annotator POS
        else:
            return "TN"  # annotator NEG


def get_outcomes(abstracted_pattern, compiled_pattern, annotations, nlp, queue):
    """Return  of pattern precision & recall measures

    Returns:
        record (dict):
    """
    # ITERATE over gold standard and

    outcomes = []  # collect TP, FP... per extract
    for set in annotations.keys():
        for annotator in annotations[set].keys():
            for entry in annotations[set][annotator]:
                text = entry[0][1]
                tags = [span[0] for span in entry[0][2]]

                # appends TP, FP, TN, FN as appropriate to list
                outcomes.append(evaluate(compiled_pattern, text, tags, nlp))

            break  # only compare against the first annotator of each set

    if any(outcomes):
         queue.put((abstracted_pattern, outcomes))


def main(argv):

    # working folder
    working_folder = argv[1]

    # number of processes
    n = int(argv[0])

    # LOAD SPACY
    nlp = spacy.load("en_core_web_sm")

    # working_folder = argv[0]

    with open("annotations.json") as f:
        annotations = json.load(f)

    # GROUP identification patterns into groups of n
    pattern_sets = [[]]
    for p in identification_patterns:
        if len(pattern_sets[-1]) == n:
            pattern_sets.append([])
        pattern_sets[-1].append(p)

    results = []

    for pattern_set in pattern_sets:

        # multiprocessing setup
        processes = []
        queue = multiprocessing.Queue()

        for abstracted_pattern in pattern_set:

            # compiled, converted pattern
            converted_pattern = convert_patterns([abstracted_pattern], chunks)[0]
            compiled_pattern = regex.compile(converted_pattern)

            # START each process (corresponding to pattern)
            process = multiprocessing.Process(
                target=get_outcomes,
                args=(abstracted_pattern, compiled_pattern, annotations, nlp, queue)
            )
            process.start()
            processes.append(process)

        # COLLECT processes
        for p in processes:
            results.append(queue.get())

        # TERMINATE processes
        for p in processes:
            process.join()


    with open(f"outcomes_{working_folder}.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1:])
