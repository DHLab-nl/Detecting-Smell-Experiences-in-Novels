"""Quick script to test hyp0: diff_mean = 0 between paired samples
Example:
    $python t_test.py working_folder1 working_folder2 cut_off
    $python t_test.py _aroma_NOUN+ADJ 0.99

Args:

Returns:
    "t_test_results.txt" summary file in working folder

Required in /working_folder
* (symbolic link to) prediction_labels_group

Notes:
    looking for set filenames in ./working_folder/set_filenames.json
    looks for sets in working folder
"""
import json
import statistics as st
import sys
from math import sqrt

from scipy.stats import t


def main(argv):

    # working folder
    wf1 = argv[0]
    wf2 = argv[1]
    cutoff = argv[2]

    # get the sets for comparison
    # {"0":"TP", ...}
    with open(f"./prediction_labels_group/group_labels_{wf1}_{cutoff}.json", "r") as f:
        set1 = json.load(f)

    with open(f"./prediction_labels_group/group_labels_{wf2}_{cutoff}.json", "r") as f:
        set2 = json.load(f)

    # CONVERT sets to form [1, 0, ...]
    set1_c = convert(set1)
    set2_c = convert(set2)

    # find the differences
    diff = [set1_c[i] - set2_c[i] for i in range(len(set1_c))]

    # t statistic - i.e., normalised diff_mean for standard t-dist comparison
    n = len(diff)
    s = st.stdev(diff)
    x = st.mean(diff)
    print(f"mean = {x}")

    t_stat = (x - 0) / (s / sqrt(n))

    # p value
    p = t.cdf(t_stat, n - 1)

    print(f"n = {n}")
    print(f"set1 - set2 mean = {x}")
    print(f"set1 - set2 st.dev = {s}")
    print(f"(C. prop > t_statistic) = {1-p}")
    print(f"(C. prop < t_statistic) = {p}")

    # print output to a text file
    with open(f"./t_test_results_@{cutoff}.txt", "w") as f:
        f.write(f"n = {n}\n")
        f.write(f"set1 - set2 mean = {x}\n")
        f.write(f"set1 - set2 st.dev = {s}\n")
        f.write(f"(C. prop > t_statistic) = {1-p}\n")
        f.write(f"(C. prop < t_statistic) = {p}\n")


def convert(set):
    """Convert, TP, FP predictions to list of 1,0s
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
