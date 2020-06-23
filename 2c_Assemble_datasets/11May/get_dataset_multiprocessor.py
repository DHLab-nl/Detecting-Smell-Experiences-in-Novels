"""create (spaCy) parsed dataset.

Example:
    $ python3 get_dataset_multiprocessor.py list.csv n

Args:
    list.csv: a list of books from which to harvest extracts.
    n (int): number of processes

Outputs:
    dataset.json {book_code: list of sentences}, where sentences are lists of word_POS
"""
import json
import multiprocessing
import os
import re
import sys

import pandas as pd
import spacy
import wget
from more_itertools import sliced
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm


def main(argv):

    dataset = {}  # container for output

    # iterate through the book list
    df = pd.read_csv(argv[0])
    for row_index, row in tqdm(df.iterrows()):

        url_code = row["code"]
        title = row["title"]
        author = row["author"]

        print(f"\n{title} by {author}\n")

        # get the book
        print("\tdownloading/reading the book")
        book_as_string = read_book(url_code)

        if book_as_string:

            # iterate over text, tokenize
            print("\nparsing the book")
            book_parsed = parse_book(book_as_string, int(argv[1]))

            dataset[url_code] = book_parsed

        else:
            print(f"failed to read {title}")

    save_file = "./datasets/output_dataset.json"
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


def parse_book(book_as_string, n):
    """Return a book as a list of (unparsed, parsed).
    Args:
        book_as_string (str):
        n (int): number of processes
    """

    # load spacy
    nlp = spacy.load("en_core_web_sm")

    # collect sentences in 'n' blocks
    sentences = [[] for i in range(n)]
    counter = 0
    for sent in sent_tokenize(book_as_string):
        sentences[counter].append(sent)
 
        if counter < 3:
            counter += 1
        else:
            counter = 0

    # parse the sentences
    processes = []
    queue = multiprocessing.Queue()
    returned = []
    for block in sentences:

        process = multiprocessing.Process(
            target=mapped_function, args=(block, nlp, queue)
        )

        process.start()
        processes.append(process)

    # collect process output
    for process in processes:
        returned += queue.get()

    # end the processes
    for process in processes:
        process.join()
    
    return returned


def mapped_function(sentences, nlp, queue):
    """return (sent, parsed_sent) version of the sentence

       remove "\n", replace "\s+" with " "
       for parased sent only, return lowercased
    """
    returned = []

    # remove \n, normalise spaces
    for sent in sentences:

        sent = sent.replace("\n", " ")
        sent = re.sub(r"\s+", " ", sent)

        doc = nlp(sent.lower())

        parsed_sent = ""  # ordered dict
        for token in doc:
            parsed_sent += f"{token.dep_}_{token.text}_{token.pos_} "


        returned.append((sent, parsed_sent))

    queue.put(returned)


if __name__ == "__main__":
    main(sys.argv[1:])  # takes a single input only
