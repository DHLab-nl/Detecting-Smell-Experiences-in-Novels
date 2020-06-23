"""
Assemble sets of extracts, taken from test.json, into x sets of y extracts.
z is the ratio of keyword extracts to random extracts.

Example:
    $ python3 assemble_test.py x y z
    $ python3 assemble_test.py 10 100 0.8

Args:
    - x (int): number of sets to assemble
    - y (int): number of extracts per set
    - z (float): proportion of extracts to contain keywords

Requires in directory:
    test.json: {"book_code": [list of sentence, parsed sentence tuples],.. }
"""

import json
import random
import sys
from collections import Counter
import math

import regex


def main(argv):

    # get commandline arguments
    number_of_sample_sets = int(argv[0])
    number_of_samples_per_set = int(argv[1])
    proportion_keywords = float(argv[2])

    # read in the test set
    with open("test.json", "r") as f:
        test_set = json.load(f)

    # read in the keywords
    with open("search_words.txt", "r") as f:
        keywords = f.readlines()
    keywords = set([w.strip("\n") for w in keywords])

    # divide the test set in to [[list of extract with keywords],[list of extracts without keywords]]
    divided_set = [[], []]
    for book_code, extracts in test_set.items():
        for extract, parsed_extract in extracts:
            if keywords.intersection(set(regex.split("\s+", extract))):
                divided_set[0].append(extract)
            else:
                divided_set[1].append(extract)

    print(f"keyword matches = {len(divided_set[0])}")

    # extract the samples
    samples = []
    total_samples = number_of_sample_sets * number_of_samples_per_set

    # keyword samples
    samples += random.sample(
        divided_set[0], math.ceil(total_samples * proportion_keywords)
    )

    # non-keyword samples
    samples += random.sample(
        divided_set[1], math.ceil(total_samples * (1-proportion_keywords))
    )

    # shuffle all samples (in-place)
    random.shuffle(samples)

    # append \n to each extract
    samples = [s + "\n\n" for s in samples]

    print(len(samples))

    # save the output

    # with open("samples.json", "w") as f:
    # json.dump(samples, f, ensure_ascii=False)

    for i in range(number_of_sample_sets):
        with open(f"./samples/test_set-{i}.txt", "w") as f:
            f.writelines(
                samples[i * number_of_samples_per_set: (i + 1) * number_of_samples_per_set]
            )


if __name__ == "__main__":
    main(sys.argv[1:])
