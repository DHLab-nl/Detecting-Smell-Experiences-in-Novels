"""Product a Histogram of measures_by_pattern data

Example:
    $ python3 histogram.py working_folder bins min max
    $ python3 histogram.py working_folder 20
    $ python3 histogram.py working_folder None None 100

Args:
    working_folder:
    bins (int): number of bins
    min (int): minimum frequency to display
    max (int): maximum frequency to display


"""
import json
import sys
from collections import Counter

import matplotlib.pyplot as plt
import statistics as st
import numpy as np


def main(argv):

    working_folder = argv[0]

    # argv
    if len(argv) > 1:
        if argv[1] != "None":
            bins = int(argv[1])
        else:
            bins = None
    else:
        bins = None

    if len(argv) > 2:
        if argv[2] != "None":
            data_min = int(argv[2])
        else:
            data_min = -1e6
    else:
        data_min = -1e6

    if len(argv) > 3:
        if argv[3] != "None":
            data_max = int(argv[3])
        else:
            data_max = 1e6
    else:
        data_max = 1e6

    with open(f"./precision_recall_stats_patterns/stats_by_pattern_{working_folder}.json", "r") as f:
        record = json.load(f)
    frequencies = [entry["P"] for pattern_abstraction, entry in record.items() if entry["P"] != "unknown"]

    sd = st.stdev(frequencies)
    print(f"standard deviation = {sd}")

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
    plt.xticks(np.arange(0, 1, step=0.1))
    plt.xlabel("Lexico-syntactic pattern precision")
    plt.ylabel("Frequency")
    plt.show()

    return len(values), min(values), max(values)


if __name__ == "__main__":
    main(sys.argv[1:])
