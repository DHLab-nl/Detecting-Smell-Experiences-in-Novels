"""Quick script to test hyp0: diff_mean = 0 between paired samples
Example:
    $python t_test.py working_folder
    $python t_test.py @0.95

Args:
    working folder to look set data

Returns:
    "t_test_results.txt" summary file in working folder

Required in /working_folder
* set 1 and set 2, i.e., {"0":"TP", ...}
* set_filenames.json ["set1.json", "set2.json"]

Notes:
    looking for set filenames in ./working_folder/set_filenames.json
    looks for sets in working folder
"""
import json
import statistics as st
from math import sqrt

from scipy.stats import t
import sys


def main(argv):

    # working folder
    wf = argv[0]

    # get filenames for set1, set2
    with open(f"./{wf}/set_filenames.json") as f:
        set1_file, set2_file = json.load(f)

    #get the sets for comparison
    # {"0":"TP", ...}
    with open(f"./{wf}/{set1_file}", "r") as f:
        set1 = json.load(f)

    with open(f"./{wf}/{set2_file}", "r") as f:
        set2 = json.load(f)

    # CONVERT sets to form [1, 0, ...]
    set1_c = convert(set1)
    set2_c = convert(set2)

    # find the differences
    diff = [set1_c[i] - set2_c[i] for i in range(len(set1_c))]

    # t statistic - i.e., normalised diff_mean for standard t-dist comparison
    n = len(diff)
    s = st.stdev(diff)
    x = st.mean(diff) ; print(f"mean = {x}")

    t_stat = (x - 0) / (s / sqrt(n))

    # p value 
    p = t.cdf(t_stat, n-1)
    print(f"(C. prop > t_statistic) = {1-p}")
    print(f"(C. prop < t_statistic) = {p}")

    # print output to a text file
    with open(f"./{wf}/t_test_results.txt", "w") as f:
        f.write(f"set1 - set2 mean = {x}\n")
        f.write(f"(C. prop > t_statistic) = {1-p}\n")
        f.write(f"(C. prop < t_statistic) = {p}\n")


def convert(set):
    """ Convert, TP, FP predictions to list of 1,0s
        TP -> 1, FN-> 0, FP or TN discarded
    """

    # converted set, 1 if "TP", 0 if "FP", ignore all others
    set_converted = []
    for index, outcome in set.items():
        if outcome == "TP":
            set_converted.append(1)
        elif outcome == "FN":
            set_converted.append(0)
        else:
            pass  # TN and FN possible, but not of interest

    return set_converted


if __name__ == "__main__":
    main(sys.argv[1:])
