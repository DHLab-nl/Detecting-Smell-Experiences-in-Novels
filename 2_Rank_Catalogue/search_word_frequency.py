"""Identifies the search word frequency wrt. search_words.txt for every book in
catalogue.json.

Example:
    $ python3 search_word_frequency.py n

Args:
    n (int): the number of processors/ threads to use.

Requires in directory:
    (a symbolic link to) catalogue (json): {"author":[(title,code),..],..}.
    search_words (txt): text file, each search word on newline.

Return:
    found.json : {frequency: [(author, title, code, (search word matches)),..], ..}
"""
import json
import math
import multiprocessing
import operator
import os
import re
import sys
import threading
from collections import Counter, defaultdict
from functools import partial, reduce

import more_itertools as mit
import regex
import wget
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map


def main(argv):

    n = int(argv[0])

    # load the catalogue
    with open("catalogue.json", "r", encoding="utf-8") as f:
        catalogue = json.load(f)  # {"author":[(title,code),..],..}

    # load the search words
    with open("search_words.txt", "r") as f:
        search_words = [word.strip() for word in f.readlines()]
        # ["smell",...]

    # convert catalogue to a single list of all books' info
    books = []
    for author, l in list(catalogue.items()):
        for title, code in l:
            books.append((author, title, code))
    # books = [(author, title, code),...]

    # (multiprocessor) scan books for
    results = filter(
        lambda x: x,
        process_map(
            partial(get_book_matches, search_words),
            books,
            max_workers=n,
            chunksize=1,
        )
    )
    print(results)
    #  results = [[freq, (author, title, code, list(set(flattened_list)))],...]

    # convert results to useful form
    returned = defaultdict(list)
    for freq, l in results:
        returned[freq] += [l]

    # output as a json
    print("returning output")
    with open("found2.json", "w") as f:
        json.dump(returned, f, indent=4, ensure_ascii=False)


def get_book_matches(search_words, book_info):
    """Return search word matches wrt. passes book.

    Args:
        search_words (list):  e.g., ["smell", "smelly",...]
        book_info (tuple): (author, title, code)

    Return:
        [freq, (author, title, code, list(set(flattened_list)))]
    """

    author, title, code = book_info
    file_name = download_book(code)

    if file_name:

        # in an try-except block because occasionally issues with reading files.
        try:

            data = sent_tokenize(read_book(file_name))
            # list of sentences

            list_by_sentence = list(map(partial(get_words, search_words), data))
            # [list_of_sentence1_search_words, list_of_sentence2_search_words,...]

            flattened_list = list(reduce(operator.concat, list_by_sentence))
            # single list of every matched word in the book (incl. repetition)

            return [len(flattened_list), (author, title, code, list(set(flattened_list)))]

        except:
            return None

    else:
        return None


def get_words(search_words, sentence):
    """Return a list of search words matches present in sentence.

    Multiple matches will result in repetition in the returned list.

    Args:
        search_words (list): list of words to search sentence for.
        sentence (str): a string segment passed.

    Returns (tuple): list of matching words
    """
    matches = map(
        lambda w: re.findall("\s+(" + w + ")[\s,.?!;]+", sentence.lower()),
        search_words,
    )  # (("smell"),...)

    matches_flattened = reduce(operator.concat, matches)

    return list(matches_flattened)


def download_book(code, suffix=False):
    """Try to download the book from PG, for given code.

    Recursively tries adding suffix, "-i" to the file name, where i = 1 to 10.
    Returns file_name or False, if successful or unsuccessful.
    """

    s = f"-{suffix}" if suffix is not False else ""
    file_name = f"{code}{s}.txt"

    try:
        url = f"https://www.gutenberg.org/files/{code}/{file_name}"
        wget.download(url, bar=None)
        return file_name
    except:
        if suffix is False:
            return download_book(code, suffix=0)
        elif suffix and suffix < 10:
            suffix += 1
            return download_book(code, suffix=suffix)
        else:
            return False


def read_book(file_name):
    """Reads a downloaded book as a string, and delete the book.

    Returns: book as a string or False
    """

    try:
        with open(file_name, "r") as f:
            data = f.read()
            os.remove(file_name)
            return data
    except:
        return False


if __name__ == "__main__":
    main(sys.argv[1:])  # takes a single input only
