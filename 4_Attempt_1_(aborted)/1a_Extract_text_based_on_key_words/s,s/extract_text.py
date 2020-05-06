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
import sys

import pandas as pd
import spacy
import wget
from more_itertools import sliced
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

    #clean up
    if os.path.exists(file_name):
        os.remove(file_name)

    return book_as_string


def parse(raw_text):
    """POS tag with flair. Sentence segmentation performed via spacy.

    Args:
        raw_text (str): A text string to be parsed.

    Returns: sentences object
    """
    # setup the libary
    nlp = spacy.load("en")

    # return the parse of raw_doc
    doc = nlp(raw_text)

    return doc


def convert_tagging_format(doc):
    """Convert doc object to wanted format.

    Args:
        doc: spacy processed text

    Return:
        a list of sentences, each sentence a list of token_tag strings
    """

    # assemble the relevant parse output features
    output = []
    for sent_index, sent in enumerate(doc.sents):
        output.append([])
        for token in sent:
            if token.pos_ != "SPACE":
                output[-1].append((token.text + "_" + token.pos_))

    return output


def extract_matches(seeds, sentences):
    """Extract sentences from 'book_as_string' that contain 'seeds' tokens.
    """
    extracts = []
    for sentence in sentences:
        overlap = list(set(seeds).intersection(set(sentence)))
        if any(overlap):
            extracts.append(sentence)

    return extracts


def main(argv, iteration_limit=None):

    extracts = {}  # container for output

    # get seed words input seedwords
    print("retrieving seed words")
    seed_file = argv[0]
    with open(seed_file, "r") as f:
        seeds = [seed.strip("\n") for seed in f.readlines()]

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

        # break book_as_string into len=1E6 chunks, and handle separately (spaCy requirement)
        if len(book_as_string) > 1000000:
            book_chunks = list(sliced(book_as_string, 1000000))
        else:
            book_chunks = [book_as_string]

        # iterate over list of book's chunks (strings)
        print("\tparsing")
        sentences = []
        for book_chunk in tqdm(book_chunks):

            # parse and convert to list of sentences
            spacy_parse = parse(book_chunk)
            sentences += convert_tagging_format(spacy_parse)

        # extract text with seed word matches
        print("\tidentifying text extracts with seed word matches")
        extracts[url_code] = extract_matches(seeds, sentences)

    save_file = "extracts.json"
    with open(save_file, "w") as f:
        json.dump(extracts, f)


if __name__ == "__main__":
    main(sys.argv[1:])  # takes a single input only
