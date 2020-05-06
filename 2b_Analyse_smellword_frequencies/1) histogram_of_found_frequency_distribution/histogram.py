"""Product a Histogram of smell key word matches by book.

Example:
    $ python3 histogram.py bins min max
    $ python3 histogram.py 20
    $ python3 histogram.py None None 100

Args:
    bins (int): number of bins
    min (int): minimum frequency to display
    max (int): maximum frequency to display


"""
import json
import sys

import matplotlib.pyplot as plt
import numpy as np


def main(argv):

    print(argv)

    # argv
    if len(argv)>0:
        if argv[0] != "None":
            bins = int(argv[0])
        else:
            bins = None
    else:
        bins = None

    if len(argv) > 1:
        if argv[1] != "None":
            data_min = int(argv[1])
        else:
            data_min = -1E6
    else:
        data_min = -1E6

    if len(argv) > 2:
        if argv[2] != "None":
            data_max = int(argv[2])
        else:
            data_max = 1E6
    else:
        data_max = 1E6

    with open("found.json", "r") as f:
        record = json.load(f)
    frequencies = [int(f) for f, books in record.items() for b in books]

    # plot histogram
    number, data_min, data_max = plot_histogram(frequencies, bins, data_min, data_max)
    print(f"{number} data points in the range {data_min} to {data_max}")

def plot_histogram(values, bins=None, minimum=None, maximum=None):
    """Plot a histogram, over the min/ max specifiied value range.

    Args:
        values
        bins (int)
        min (int)
        max (int)

    Returns:
        number of values in specified range, range min, range max
    """
    if minimum:
        values = [v for v in values if v >= minimum]

    if maximum:
        values = [v for v in values if v <= maximum]

    # sturges' bins
    if bins is None:
        bins = int(round(1 + 3.322 * np.log10(len(values)), ndigits=0))

    # histogram
    plt.hist(values, bins=bins)
    plt.show()

    return len(values), min(values), max(values)


if __name__ == "__main__":
    main(sys.argv[1:])
