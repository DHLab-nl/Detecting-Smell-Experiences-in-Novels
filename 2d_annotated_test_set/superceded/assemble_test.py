"""
Assemble a set of extracts, taken from test.json at random (even number of samples form each book, taken at random)

Example:
    $ python3 assemble_test.py 6000 20

Args:
    - total number of extracts to retrieve (int)
    - total number of test sets to divide the extracts into

Requires in directory:
    harvesting.json: {"book_code": [list of sentence, parsed sentence tuples],.. }

Note: if 80 000 is a typical novel size and 20 is a typical word size, a novel may have 4000 sentences on average. starting with 500 extracts.
 
"""

import random
import sys
from collections import Counter

import json


def main(argv):

    # saving output
    samples = []
    sample_distribution = Counter()

    # number of samples to get
    number_of_samples = int(argv[0])
    number_of_sets = int(argv[1])

    # read in the test set
    with open("test.json", "r") as f:
        test_set = json.load(f)

    number_of_books = len(test_set)

    # iterate through books and extract samples
    for book_code, extracts in test_set.items():
        samples.append([])
        for i in range(int(number_of_samples / number_of_books)):
            extract, parsed_extract = random.choice(extracts)
            samples[-1].append(extract + "\n")
            sample_distribution[book_code] += 1

    # save the output
    with open("test_set_samples.json", "w") as f:
        json.dump(samples, f, ensure_ascii=False)

    for sample_index, sample in enumerate(samples):
        with open(f"test_set_samples-{sample_index}.txt", "w") as f:
            f.writelines(sample)

    # info on sample distribution
    print("sampling distribution by book")
    for book_code in list(sample_distribution.keys()):
        print(book_code, sample_distribution[book_code])


if __name__ == "__main__":
    main(sys.argv[1:])
