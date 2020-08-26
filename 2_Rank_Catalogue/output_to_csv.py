"""Convert found.json to csv: freq, title, author, words, code.

Example:
    $ python3 output_to_csv.py

Requires in directory:
    found.json : output from search_word_frequency.py

Return:
    found.csv
"""
import json

import numpy as np
import pandas as pd


def main():

    with open("found.json", "r") as f:
        found = json.load(f)  
        # found = {freq:[[author, title, code, [words]],..], ..

    # populate a list with relevant info from found.json
    data = []  # data[i] = row i info for (to be created)
    for freq in sorted(found.keys(), key=lambda x: int(x), reverse=True):
        books = found[freq]
        for book in books:
            author = book[0]
            title = book[1]
            code = book[2]
            words = book[3]

            entry = [freq, title, author, words, code]
            data.append(entry)

    # convert to/ create csv from data variable
    df = pd.DataFrame(data, columns=["freq.", "title", "author", "words", "code"])
    df.to_csv("found.csv")


if __name__ == "__main__":
    main()
