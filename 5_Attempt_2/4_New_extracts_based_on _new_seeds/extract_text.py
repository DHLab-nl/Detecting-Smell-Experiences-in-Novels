"""Iterate over harvesting.csv entries and extract sentences with seed words.

Example:
    $ python3 new_extracts.py

Outputs:
    new_extracts.json {book_code: list of sentences}, where sentences are lists of word_POS
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
        pass

    # clean up
    if os.path.exists(file_name):
        os.remove(file_name)

    return book_as_string


def main():

    extracts = {}  # container for output

    # load the seed words
    print("retrieving seed words")
    lexicon_file = "lexicon.json"
    with open(lexicon_file, "r") as f:
        lexicon = json.load(f)

    # load previous extracts
    previous_extracts_file = "previous extracts.json"
    with open(previous_extracts_file, "r") as f:
        previous_extracts = json.load(f)

    # iterate through the book list
    df = pd.read_csv("harvesting.csv")
    for row_index, row in df.iterrows():

        url_code = row["code"]
        title = row["title"]
        author = row["author"]

        print(f"\n{title} by {author}\n")

        # get the book
        print("\tdownloading/reading the book")
        book_as_string = read_book(url_code)

        book_extracts = []
        print("\tsentence_segmentation")
        for sentence in sent_tokenize(book_as_string):

            # set of current sentence's lowercased tokens
            token_set = set([token.lower() for token in word_tokenize(sentence)])
            # iterate over seeds, checks for seeds in sentence's token set
            for pattern, seeds in lexicon.items():
                for seed in seeds:

                    # get seed and seed overlap with sentence as sets
                    seed = set(seed)
                    overlap = seed.intersection(token_set)

                    # overlap == seed, then we have a match
                    if overlap == seed:
                        # standardard extracts
                        amended_sentence = sentence.replace("\n", " ")
                        amended_sentence = re.sub(r"\s+", " ", amended_sentence,)
                        amended_sentence = amended_sentence.lower()

                        # retain only new extracts, check against previous
                        if amended_sentence not in previous_extracts:
                            book_extracts.append(amended_sentence)

        if any(book_extracts):
            extracts[url_code] = book_extracts

    save_file = "extracts.json"
    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(extracts, f, ensure_ascii=False)


if __name__ == "__main__":
    main()  # takes a single input only
