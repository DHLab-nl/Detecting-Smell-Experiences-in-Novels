"""Create (spaCy) parsed dataset.

The text is decomposed into constituent sentences, each sentence passed to spaCy separately.
Each token (word) in the passed sentences is appended with the dependency and POS tags.

Example:
    $ python3 get_dataset.py list.csv n

Args:
    list.csv: a list of books from which to harvest extracts.
    n (int): number of processes

Outputs:
    datasets/output_dataset.json : {book_code: list of sentences}, where sentences are lists of dep_word_POS
"""
import json
import math
import os
import re
import sys
from functools import partial

import more_itertools as mit
import pandas as pd
import spacy
import wget
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map


def main(argv):

    n = int(argv[1])

    # read in the dataset csv
    df = pd.read_csv(argv[0])

    # convert df to list of books
    books = list(df.values)
    # = [(index, frequency, title, author, ["pungent",...], code),... ]

    # load the spaCy nlp lib
    nlp = spacy.load("en_core_web_sm")

    parses = list(process_map(partial(get_dataset, nlp), books, max_workers=n))
    # parses = [(code,[(normalised_sentence, parsed_sentence),...]),...]

    dataset = {parse[0]: parse[1] for parse in parses if parse is not None}
    # {code:[(sentence1 text, sentence1 parse),...],... }

    with open("./datasets/dataset.json", "w") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)


def get_dataset(nlp, df_entry):
    """Return (code,[(normalised_sentence, parsed_sentence),...])
    """

    code = df_entry[-1]

    file_name = get_book(code)
    if file_name:
        try:
            data = read_book(file_name)

            # results = []
            # for sent in tqdm(sent_tokenize(data)):
            #     results.append(partial(get_parse, nlp)(sent))
            # return (code, results)

            return (code, list(map(partial(get_parse, nlp), sent_tokenize(data))))
            # results = (code,[(normalised_sentence, parsed_sentence),...]), for book
        except:
            print(f"reading {code} failed")
            return None
    else:
        return None


def get_parse(nlp, unparsed_sentence):
    """Return (normalised_sentence, parsed_sentence) for the passed
    unparsed_sentence.
    """

    # create a lowercased form, remove \n and normalise spaces
    s = re.sub(r"\s+", " ", unparsed_sentence.replace("\n", " ")).lower()

    # parse the string in the form
    doc = nlp(s)
    parse = lambda t: f"{t.dep_}_{t.text}_{t.pos_}"
    parsed_sentence = " ".join(map(parse, doc))

    return (s, parsed_sentence)


def get_book(code, suffix=False):
    """Download the book from PG, for given code.

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
            return get_book(code, suffix=0)
        elif suffix and suffix < 10:
            suffix += 1
            return get_book(code, suffix=suffix)
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
