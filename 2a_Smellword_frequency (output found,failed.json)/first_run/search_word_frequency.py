"""
Written by RJB 2020

Identify the search word frequency for every book in the .json catalogue

Example:
    $ python3 search_word_frequency.py catalogue.json search_words.txt

Args:
    catalogue (json): {"author":[(title,code),..],..}
    search_words (txt): text file, each search word on newline

Return:
    {frequency: (author, title, code, (search word matches)), ..}
"""
import json
import os
import sys
from collections import Counter

import wget
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm


def main(argv):

    assert (
        len(argv) == 2
    ), "call python3 search_word_frequency.py catalogue search_words"

    # load the catalogue
    with open(argv[0], "r") as f:
        catalogue = json.load(f)  # {"author":[(title,code),..],..}

    # load the search words
    with open(argv[1], "r") as f:
        search_words = [word.strip() for word in f.readlines()]  # []

    # container to store return
    returned = {}  # {frequency: [( author, title, code, (matches) ), ..]}

    # read fail
    read_fail = [] # 

    # iterate catalogue books/ book codes
    for author in tqdm(catalogue.keys()):
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

            # with open("found.json", "w") as f:
            #     json.dump(returned, f)

            # with open("failed.json", "w") as f:
            #     json.dump(read_fail, f)

    with open("found.json", "w") as f:
        json.dump(returned, f)

    with open("failed.json", "w") as f:
                json.dump(read_fail, f)


if __name__ == "__main__":
    main(sys.argv[1:])  # takes a single input only
