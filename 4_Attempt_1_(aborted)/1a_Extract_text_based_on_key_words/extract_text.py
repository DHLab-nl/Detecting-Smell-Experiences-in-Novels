"""Iterate over literature.csv entries and extract sentences with seed words.

Example:
    $ python3 extract_text.py seed_file.txt

Args:
    seed_file.txt: a list of word_POS seeds, one on each line

Outputs:
    extracts.json {book_code: list of sentences}, where sentences are lists of word_POS
"""
import json
import os
import re
import sys

import pandas as pd
import spacy
import wget
from more_itertools import sliced
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm


def read_book(code):
    """Download and return a book code as a string

    Args:
        code (string): PJ book code to download and read

    Returns:
        book as a string. None if could not download or read successfully.
    """
    # download book
    file_name = None
    try:
        file_name = f"{code}.txt"
        url = f"https://www.gutenberg.org/files/{code}/{file_name}"
        wget.download(url, bar=None)
    except:
        # failed? try to find with file suffix 1-10
        for i in range(0, 11):
            try:
                file_name = f"{code}-{i}.txt"
                url = f"https://www.gutenberg.org/files/{code}/{file_name}"
                wget.download(url, bar=None)
                break  # break if works
            except:
                pass

    # try to read book
    book_as_string = None
    try:
        with open(file_name, "r") as f:
            book_as_string = f.read()
    except:
        # print(f"{file_name} read failed")
        read_fail.append(code)

    # clean up
    if os.path.exists(file_name):
        os.remove(file_name)

    return book_as_string


def main(argv, iteration_limit=None):

    extracts = {}  # container for output

    # get seed words input seedwords
    print("retrieving seed words")
    seed_file = argv[0]
    with open(seed_file, "r") as f:
        seeds = set([seed.strip("\n") for seed in f.readlines()])

    # iterate through the book list
    df = pd.read_csv("literature.csv")
    for row_index, row in df.iterrows():

        url_code = row["code"]
        title = row["title"]
        author = row["author"]

        print(f"\n{title} by {author}\n")

        # get the book
        print("\tdownloading/reading the book")
        book_as_string = read_book(url_code)

        # iterate over list of book's chunks (strings)
        print("\tsentence_segmentation")

        book_extracts = []
        for sentence in sent_tokenize(book_as_string):
            token_set = set([token.lower() for token in word_tokenize(sentence)])
            overlap = list(seeds.intersection(token_set))

            if any(overlap):
                # save sentences matching seed words, replace \n in text
                amended_sentence = sentence.replace("\n", " ")
                amended_sentence = re.sub(r"\s+", " ", amended_sentence, )
                book_extracts.append(amended_sentence)

        if any(book_extracts):
            extracts[url_code] = book_extracts

    save_file = "extracts.json"
    with open(save_file, "w") as f:
        json.dump(extracts, f)


if __name__ == "__main__":
    main(sys.argv[1:])  # takes a single input only
