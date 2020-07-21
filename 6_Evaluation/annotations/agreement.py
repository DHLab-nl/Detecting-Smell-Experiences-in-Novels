"""Check inter-annotator agreement.
     create agreement_{set}.json
     report cohen's kappa and proportion of agreement in terminal

Example:
    $python3 agreement.py set contains
    $python3 agreement.py set0 "['d', 'o']"

Args:
    set (str): which set to examine for inter-annotator agreement
    contains (list): a list of tags, where any one present (even if differendt) in two annotators' annotations wrt. an extract, then both deemed in agreement

Requires in dir:
    Annotations.json
        # {"set0":
              # by-annotator dict of extracts/ annotations
        #     {
                  # list of annotator:extract dicts wrt. set
        #         "annotator1":
        #         [
                      # extract & annotations within extract
        #             (
                          index,
        #                 extract_text,
        #                 [(label, annotation),...]
        #             ),
        #             ...
        #         ],
        #         ...
        #     },
        #     ....

        # }
"""
import itertools
import json
import os
import sys

import numpy as np
import scipy.stats as st


def main(argv):

    set = argv[0]

    # IMPORT annotations.json
    with open("annotations.json", "r") as f:
        annotations = json.load(f)

    # REORGANISE the set's data into a more useful form
    tagged_extracts = __get_data(annotations, set)
    # extract:{"annotator1":["d"], ...}, ...]

    with open(f"agreement_{set}.json", "w") as f:
        json.dump(tagged_extracts, f, indent=4, ensure_ascii=False)

    # HACK - TO USE MANUALLY EDITED FILE!
    # with open(f"agreement_{set}.json", "r") as f:
        # tagged_extracts = json.load(f)


    # measure inter-annotator agreement
    kappas = []
    proportions = []

    contains = eval(argv[1])
    annotators = list(annotations[set].keys())
    for i in range(len(annotators)):
        annotator1 = annotators[i]
        for j in range(i + 1, len(annotators)):
            annotator2 = annotators[j]
            k, po, results_matrix = cohen(
                tagged_extracts, contains, annotator1, annotator2
            )
            proportions.append((annotator1, annotator2, po))
            kappas.append((annotator1, annotator2, k))

            # print(results_matrix)

    print(f"kappas: {kappas}")
    print(f"proportions: {proportions}")

def cohen(tagged_extracts, contains, annotator1, annotator2):
    """yes,yes result is when both annotator's extract annotations match at least one entry in contains list
    e.g., if A="a" and B="b", contains = ["a", "b"] then it's a yes,yes (agreement)
    Args:
        tagged_extracts = {"index":[text, {"annotator1":[],...}],,...}
        tagged_extracts: [extract:{"annotator1":["d"], ...}, ...]
    """
    print(len(tagged_extracts))
    # STORE agreements and disagreements
    results_matrix = np.zeros((2, 2))
    # [[Ayes-Byes, Ayes-Bno],[Ano-Byes, Ano-Bno]]

    # ITERATE over the extracts and populate the matrix
    for index, data in tagged_extracts.items():

        A = itertools.chain.from_iterable(data[1][annotator1]) # tag set
        B = itertools.chain.from_iterable(data[1][annotator2]) # tag set

        # A = yes
        if any(set(contains).intersection(set(A))):
            # B = yes
            if any(set(contains).intersection(set(B))):
                results_matrix[0, 0] += 1
            # B = no
            else:
                results_matrix[0, 1] += 1
        else:
            # B = yes
            if any(set(contains).intersection(set(B))):
                results_matrix[1, 0] += 1
            # B = no
            else:
                results_matrix[1, 1] += 1

    # Calculate kappa

    a, b, c, d = (
        results_matrix[0, 0],
        results_matrix[0, 1],
        results_matrix[1, 0],
        results_matrix[1, 1],
    )
    print(annotator1, annotator2, a, b, c, d)
    po = (a + d) / (a + b + c + d)  # proportion of agreement
    pYes = ((a + b) / (a + b + c + d)) * ((a + c) / (a + b + c + d))
    pNo = ((c + d) / (a + b + c + d)) * ((b + d) / (a + b + c + d))

    pe = pYes + pNo
    k = (po - pe) / (1 - pe)

    return k, po, results_matrix


def __get_data(annotations, set):
    """Return {extract:{"annotator1":["d"],...}, ...}, for the specified set
       Return {index:[extract_text, {"annotator1":["d"],...}], ...}, for the specified set
    Args:
        annotations:
        set (string): set for which to assemble data for comparison
    """

    # texts = [(0, *"what is this life if..."), (1, "I'm the very model of a ...")]
    texts = []
    for annotator in annotations[set]:
        for entry in annotations[set][annotator]:
            text = (entry[0][0], entry[0][1])
            texts.append(text)

    # tagged_extracts = {"index":[text, {"annotator1":[],...}],,...}
    tagged_extracts = {}
    for index, text in texts:
        tagged_extracts[index] = [text, {}]
        # initialise each annotator
        for annotator in annotations[set]:
            tagged_extracts[index][1][annotator] = []

    # populate
    # tagged_extracts = {text:{"annotator1":["d"], ...}, ...}
    for annotator in annotations[set]:
        for entry in annotations[set][annotator]:
            index = entry[0][0]
            tags = [spans[0] for spans in entry[0][2]]


            if any(tags):
                tagged_extracts[index][1][annotator].append(tags)

    return tagged_extracts


if __name__ == "__main__":
    main(sys.argv[1:])
