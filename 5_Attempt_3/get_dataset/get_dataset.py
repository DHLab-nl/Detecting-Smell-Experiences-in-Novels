"""create (spaCy) parsed dataset.

Example:
    $ python3 create_set.py

Args:
    harvesting.csv: a list of books from which to harvest extracts.

Outputs:
    dataset.json {book_code: list of sentences}, where sentences are lists of word_POS
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


def main():

    dataset = {}  # container for output

    # iterate through the book list
    df = pd.read_csv("harvesting.csv")
    for row_index, row in tqdm(df.iterrows()):

        url_code = row["code"]
        title = row["title"]
        author = row["author"]

        print(f"\n{title} by {author}\n")

        # get the book
        print("\tdownloading/reading the book")
        book_as_string = read_book(url_code)

        # iterate over text, tokenize
        print("\nparsing the book")
        book_parsed = parse_book(book_as_string)

        dataset[url_code] = book_parsed

    save_file = "dataset.json"
    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False)


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


def parse_book(book_as_string):
    """Return a book as a list of (unparsed, parsed).
    """
    parses = []

    # load spacy
    nlp = spacy.load("en_core_web_sm")

    # parse the sentences
    for sent in sent_tokenize(book_as_string):

        # remove \n
        sent = sent.replace("\n", " ")
        sent = re.sub(r"\s+", " ", sent)

        doc = nlp(sent.lower())
        parsed_sent = ""  # ordered dict

        for token in doc:
            parsed_sent += f"{token.dep_}_{token.text}_{token.pos_} "

        parses.append((sent, parsed_sent))

    return parses


if __name__ == "__main__":
    main()  # takes a single input only
