"""Produce a boxplot of smell keyword matches by book.

Requires:
    found.json: A symbolic link to found.json

Args:
    (optional)
    min (float): values below min disregarded
    max (float): values above max disregarded

Example:
    $ python3 boxplot.py min max
"""
import json
import sys

import matplotlib.pyplot as plt
import numpy as np


def main(argv):

    # argv
    if not any(argv):
        data_min = None
        data_max = None
    else:
        data_min = int(argv[0])
        data_max = int(argv[1])

    # get data
    with open("found.json", "r") as f:
        found = json.load(f)  # found = {freq:[author, title, code, [],..], ..}

    # if max/ min specified, amend data range
    if data_min!=None and data_max!=None:
        frequencies = [
            int(f)
            for f, books in found.items()
            for b in books
            if int(f) >= data_min and int(f) <= data_max
        ]
    else:
        frequencies = [int(f) for f, books in found.items() for b in books]

    print(data_min, data_max)
    # print(frequencies)

    # plot boxplot
    plt.boxplot(frequencies)
    plt.show()

    # get the range of statistical outliers
    print(f"mean +/- 2sd: {np.mean(frequencies)} +/- {2*np.std(frequencies)}")


if __name__ == "__main__":
    main(sys.argv[1:])
