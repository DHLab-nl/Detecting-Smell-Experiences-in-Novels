"""Get the estimated precisions of patterns in validation_patterns.json

Example:
    $python3 validation_statistics.py subfolder

Args:
    subfolder (string): subfolder to find validation_patterns.json, annotated validation extracts by pattern

"""
import json
import math
import sys

from scipy.stats import norm


def main(argv):

    folder = argv[0]

    # get list of previously validated patterns
    with open(folder + "/validated_patterns.json", "r") as f:
        validation_patterns = json.load(f)

    # iterate over validation patterns and
    for pattern in validation_patterns:
        print(f"current pattern: {pattern}")
        with open(folder + f"/validation_{pattern}.json", "r") as f:
            j = json.load(f)

        # get point estimate of statistics and calculate 90% CI lowerbound
        precision, total_count, unknown_count = get_precision(pattern, j)
        # CI_lowerbound = get_lb_CI(precision, total_count, unknown_count)

        print_nice(pattern, precision, total_count, unknown_count, 0)


def get_lb_CI(point_estimate, total_count, unknown_count):
    """Return the lowerbound 90% CI corresponding to a point estimate.

        precision is our point estimate of the true precision wrt. the population, i.e. all extracts pulled out by the pattern.

        precision = TP/(TP + FP)
        i.e., a ratio of summations, so central limit theorem applies
    """
    p = point_estimate
    q = 1 - p
    sigma = math.sqrt(p * q / (total_count - unknown_count))
    E = norm.ppf(0.95) * sigma
    CI_lowerbound = p - E

    return CI_lowerbound


def print_nice(pattern, precision, total_count, unknown_count, CI_lowerbound):
    """
    """
    print("\n\n")
    print(f"{pattern}")
    print(f"\tprecision point estimate = {precision}")
    print(f"\tprecision lowerbound CI = {CI_lowerbound}")
    print(f"\ttotal count = {total_count}")
    print(f"\tunknown count = {unknown_count}")


def get_precision(pattern, j):
    """ Calculate the precision in a validation json file.
    """
    TP = 0
    FP = 0
    U = 0
    counter = 0

    for extract in j:
        if extract[2] == "TP":
            TP += 1
        elif extract[2] == "FP":
            FP += 1
        elif extract[2] == "U":
            U += 1
        else:
            print(f"{pattern}, unknown tag: {extract[2]}")
            exit(1)
        counter += 1

    return TP / (TP + FP), counter, U


if __name__ == "__main__":
    main(sys.argv[1:])
