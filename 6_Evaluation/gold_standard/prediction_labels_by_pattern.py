"""Return a list of [TN, TP, FP, FN,..] outcomes for each extract by pattern,
wrt. each sentence in the gold standard. A positive match is deemed a positive
outcome to the question "is the sentence a smell experience". The gold standard
tags"d" and "o" represent the presence of a smell experience in text for which
to judge against.

Example:
    $python3 prediction_labels_by_pattern.py n working_folder
    $python3 prediction_labels_by_pattern.py n _aroma_NOUN+VERB

Requires in Directory:
    * (a symbolic link to) annotations.json

Returns:
    outcomes_{working_folder}.json : [ (identification pattern, [**]), ...]

    where ** is a list of TP/TN/FP/FN labels correspoding to the each gold
    standard sentence annotation.

    Only the first annotator of each set is considered.
"""
import json
import math
import os
import re
import sys
from functools import partial

import numpy as np
import regex
import spacy
from tqdm.contrib.concurrent import process_map

# add libraries to path
sys.path.append(os.path.join(sys.path[0], "libraries"))
# add working folder to path
sys.path.append(os.path.join(sys.path[0], sys.argv[2]))

from CHUNKS import chunks
from pattern_abstraction import convert_patterns
from PATTERNS import identification_patterns


def evaluate(compiled_pattern, text, tags, nlp):
    """Return one of TP,TN,FP,FN wrt. compiled pattern, text and gold standard
    tags corresponding to the text.

    I.e.,
    A pattern match, equates to a "positive" prediction.
    The user annotations represent the ground truth.
    Thus:
        * pattern match + "o" or "d" tags == TP
        * pattern match w/o tags == FP
        * no match + "o or "d" tags == FN
        * no match w/o tags == TN
    """

    # parse text with space
    text_parsed = ""
    doc = nlp(re.sub(r"\s+", " ", text.lower().replace("\n", " ")))
    for token in doc:
        text_parsed += f"{token.dep_}_{token.text}_{token.pos_} "

    # search for a match between pattern and parsed text
    mo = regex.search(compiled_pattern, text_parsed)
    if mo:  # pattern predicts IS a smell experience
        if "d" in tags or "o" in tags:
            return "TP"
        else:
            return "FP"
    if not mo:  # pattern predicts NOT a smell experience
        if "d" in tags or "o" in tags:
            return "FN"
        else:
            return "TN"


def get_outcomes(annotations, nlp, p):
    """Return a list of [TP,TN,FP,FN] for the input pattern's performance wrt. text extracts and the gold standard tags 

    Args:
        annotations (dict):
        nlp:
        p (tup): (pattern_abstraction, regex compiled form)

    Returns:(pattern_abstraction, [**]) , where [**] is a list of TP/TN/FP/FN
    prediction outcomes for each sentence in the gold standard.

    *Considers only the first annotator of each set*
    """
    pattern_abstraction, compiled_pattern = p

    # ITERATE over gold standard
    outcomes = []  # collect TP, FP... per extract
    for set in annotations.keys():
        for annotator in annotations[set].keys():
            for entry in annotations[set][annotator]:
                text = entry[0][1]  # complete extract text
                tags = [
                    span[0] for span in entry[0][2]
                ]  # list of all tags annotator associates with text

                # appends TP, FP, TN, FN as appropriate
                outcomes.append(evaluate(compiled_pattern, text, tags, nlp))

            break  # only compare against the first annotator of each set

    if any(outcomes):
        return (pattern_abstraction, outcomes)


def get_compiled_patterns(pattern_abstraction):
    """Return (pattern_abstraction, regex compiled version)"""

    converted_pattern = convert_patterns([pattern_abstraction], chunks)[0]
    compiled_pattern = regex.compile(converted_pattern)

    return (pattern_abstraction, compiled_pattern)


def main(argv):

    # working folder
    working_folder = argv[1]

    # number of processes
    n = int(argv[0])

    # LOAD SPACY
    nlp = spacy.load("en_core_web_sm")

    # load annotations
    with open("annotations.json") as f:
        annotations = json.load(f)

    # create list of (pattern, compiled_pattern) for all patterns
    patterns = list(map(get_compiled_patterns, identification_patterns))
    # [(pattern, compiled_pattern),...]

    print("Assembling a list of pattern prediction outcomes by sentence")
    print("iterating over each pattern...")
    results = process_map(
        partial(get_outcomes, annotations, nlp),
        patterns,
        max_workers=n,
        chunksize=1,
    )
    # [(pattern_abstraction, [**]),..]
    # where [**] is a list of TP, FN, FP, TN labels for each sentence

    # save to json
    with open(f"./prediction_labels_patterns/prediction_labels_{working_folder}.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1:])
