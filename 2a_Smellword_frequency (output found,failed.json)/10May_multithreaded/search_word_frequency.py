"""
Written by RJB 2020

Identify the search word frequency for every book catalogue.json

Example:
    $ python3 search_word_frequency.py

Requires in directory:
    catalogue (json): {"author":[(title,code),..],..}
    search_words (txt): text file, each search word on newline

Return:
    {frequency: (author, title, code, (search word matches)), ..}
"""
import json
import os
import sys
import threading
from collections import Counter
import regex

import wget
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm


def main():

    # load the catalogue
    with open("catalogue.json", "r") as f:
        catalogue = json.load(f)  # {"author":[(title,code),..],..}

    # load the search words
    with open("search_words.txt", "r") as f:
        search_words = [word.strip() for word in f.readlines()]

    # container to store return
    returned = {}  # {frequency: [( author, title, code, (matches) ), ..]}
    read_fail = []  # list of url_codes

    # approx 3000 authors each split/ thread
    splits = [
        "[Aa].*",
        "[BbCcDd].*",
        "[EeFf].*",
        "[Gg],*",
        "[HhIi]",
        "[Jj]",
        "[KkLlMm].*",
        "[NnOoPpQqRr].*",
        "[SsTtUu].*",
        "[WwXxYyZz].*",
        "[Vv].*",
    ]

    threads = []  # collect the threads

    # run multiple processes
    print("scanning for seed words, as a multi-threaded process")
    for split in splits:
        
        # collect all of the authors that are in the split
        authors = []
        for author, books in catalogue.items():
            mo = regex.match(split, author)
            if mo:
                authors.append(author)

        # create a thread object, and start the scan
        process = threading.Thread(
            target=get_seeds_frequencies,
            args=(authors, catalogue, search_words, returned, read_fail),
        )
        process.start()
        threads.append(process)

    # collect output from multiple threads
    for process in threads:
        process.join()
    print("collecting output from threads")

    # output as a json
    print("returning output")
    with open("found.json", "w") as f:
        json.dump(returned, f)


def get_seeds_frequencies(authors, catalogue, search_words, returned, read_fail):
    """
    """
    # iterate catalogue books/ book codes
    for author in tqdm(authors):
        for book_details in catalogue[author]:

            title = book_details[0]
            code = book_details[1]

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
            try:
                with open(file_name, "r") as f:
                    data = f.read()
            except:
                # print(f"{file_name} read failed")
                read_fail.append(code)
                if os.path.exists(file_name):
                    os.remove(file_name)
                continue

            # iterate through sentences in a document, find matches
            matches = Counter()  # {search_word:count,..}
            for sentence in sent_tokenize(data):

                # find match between search_terms and sentence tokens
                for match in set(search_words).intersection(
                    set([w.lower() for w in word_tokenize(sentence)])
                ):
                    # print(match)
                    matches[match] += 1

            # delete the downloaded book
            if os.path.exists(file_name):
                os.remove(file_name)

            # store in container
            frequency = sum(matches.values())
            if frequency not in returned.keys():
                returned[frequency] = []

            returned[frequency].append((author, title, code, (list(matches.keys()))))


if __name__ == "__main__":
    main()  # takes a single input only
