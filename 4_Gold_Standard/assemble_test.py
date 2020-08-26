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
    (a symbolic link to...)
    test.json: {"book_code": [(sentence, parsed_sentence),...],.. }
"""
import json
import math
import operator
import random
import re
import sys
from functools import partial, reduce

from tqdm.contrib.concurrent import process_map


def main(argv):

    # get commandline arguments
    n = int(argv[0])  # number of sets
    r = int(argv[1])  # number of samples per set
    k = float(argv[2])  # proportion of samples to contain search words

    print("reading in the test set")
    with open("test.json", "r") as f:
        test_set = json.load(f)
        # {"book_code": [(sentence, parsed_sentence),...],...}

    print("reading in the search words")
    with open("search_words.txt", "r") as f:
        search_words = f.readlines()
    search_words = [w.strip("\n") for w in search_words]
    # [word,..]

    print("getting a list of sentences, by book")
    sentences_by_book = map(lambda x: [i[0] for i in x[1]], test_set.items())
    # [book0_list_of_sentences,..] iterator

    print("separating sentences into those with and wihout search words")
    sorted_by_book = process_map(
        partial(sort_book, search_words), list(sentences_by_book), max_workers=4
    )
    # [(book0_list_with_searchwords, book0_list_with_searchwords),..] iterator

    # split these into two separate lists
    print("assembling a list of sentences with search words")
    sentences_containing = reduce(operator.concat, map(lambda b: b[0], sorted_by_book))

    print("assembling a list of sentences absent of search words")
    sentences_absent = reduce(operator.concat, map(lambda b: b[1], sorted_by_book))

    print("sampling the required number of extracts from the dataset")
    samples_containing = random.sample(sentences_containing, math.ceil(n * r * k))
    samples_absent = random.sample(sentences_absent, math.ceil(n * r * (1 - k)))

    print("saving...")
    for i in range(n):
        sample = (
            samples_containing[int(i * r * k) : int((1 + i) * r * k)]
            + samples_absent[int(i * r * (1 - k)) : int((1 + i) * r * (1 - k))]
        )
        with open(f"./samples/test_set-{i}.txt", "w") as f:
            f.writelines([s + "\n\n" for s in sample])


def sort_book(search_words, book):
    """Return a list of sentences as (list_with_words, list_without_words).

    Args:
        search_words (list): list of search words.
        book (list): list of sentences.
    """

    # list of sentences containing (at least one) search word
    with_sw = filter(
        lambda x: x, map(lambda s: s if contains(search_words, s) else None, book)
    )
    # [sentence,...] iterator

    # list of sentences containin no search words
    without_sw = filter(
        lambda x: x, map(lambda s: s if not contains(search_words, s) else None, book)
    )
    # [sentence,...] iterator

    return (list(with_sw), list(without_sw))


def contains(search_words, sentence):
    """Return True if sentence contains any search_word, otherwise False."""

    # list of search words
    found = filter(
        lambda x: x,
        map(
            lambda w: w if re.search("\\s(" + w + ")[\\s,.!?;]+", sentence) else None,
            search_words,
        ),
    )
    # [word,..] iterator

    if len(list(found)) > 0:
        return True
    else:
        return False


if __name__ == "__main__":
    main(sys.argv[1:])
