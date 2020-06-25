"""A script which does 2 things, wrt. a specified working_folder, i.e., implementation.

    1) Calculate by-pattern recall & precision from TP, TN, FP ...  from "outcome_{working_folder}.json".
       output file : "measures_by_pattern_{working_folder}.json"
       This is irrespective of threshold command line arg

    2) determine the TP, FP, ... outcomes for group prediction based on the
    patterns in working_folder. This is wrt. to some threshold precision, below
    which a pattern is ignored from group prediction.
    output file "group_results_{working_folder}.json"

    group prediction: if a single pattern (included) predicted Positive (is an
    extract), the group prediction is Positive (is an extract)

    e.g., consider a group of 2 patterns, used for group prediction
    if extract if positive (is a smell):
        possible simultaneous pattern outcomes:
            TP, TP or TP, FN or FN, FN
            thus, the group pred = TP or FN, no other possibilities

    if extract is negative (not a smell):
        possible simultaneous pattern outcomes:
            TN, TN or TN, FP or FP, FP, no other possbilities

    Thus, if TP or FP occurs in a single pattern, the group prediction is positive
    if no instance of TP or FP occurs then all patterns will be the same, one of TN or FN, group prediction is same

Calculate the precision and recall by pattern.
   output a json file

Example:
    $python3 measures_by_pattern.py working_folder cutoff
    $python3 measures_by_pattern.py _aroma_NOUN+ADJ/ 0.90

working_folder (string): folder containing PATTERNS.py of interest

Returns:
    measures_by_pattern_{working_folder}.json
    (terminal) precision & recall value for global group, for patterns p >= cutoff
"""
import json
import sys

def main(argv):

    working_folder = argv[0]
    cutoff = float(argv[1])

    with open(f"outcomes_{working_folder}.json", "r") as f:
        outcomes = json.load(f)

    # determine the by-pattern recall and precision
    measurements = {}
    # {"pattern":{"P":0.4 , "R":0.2}}
    for entry in outcomes:
        pattern_abstraction = entry[0]
        pattern_outcomes = entry[1]

        # print(pattern_abstraction)

        TP = pattern_outcomes.count("TP")
        FP = pattern_outcomes.count("FP")
        TN = pattern_outcomes.count("TN")
        FN = pattern_outcomes.count("FN")

        # print(TP, FP)

        measurements[pattern_abstraction] = {}
        epsilon = 1E-6
        measurements[pattern_abstraction]["P"] = TP / (TP + FP + epsilon)
        measurements[pattern_abstraction]["R"] = TP / (TP + FN + epsilon)

        # change to 'unknown' where no matching extracts available
        # i.e., where TP + FP = 0
        if TP + FP == 0:
            measurements[pattern_abstraction]["P"] = 'unknown'
            measurements[pattern_abstraction]["R"] = 'unknown'

    with open(f"measures_by_pattern_{working_folder}.json", "w") as f:
        json.dump(measurements, f, indent=4)

    #
    # global recall
    # 
    # any one pattern predicts true, the collective is True
    #   if an extract is positive, pattern predictions can only be TP or FN
    #       thus, group takes TP is a single is TP, otherwise FN 
    #   if an extract is negative, pattern predictions can only be TN or FP
    #       thus, the group takes FP is a single FP, otherwise TN

    group_results = {}
    # {extract_index:[list of outcomes by pattern]}

    # collect group results
    for entry in outcomes: # each entry corresponds to a pattern
        pattern_abstraction = entry[0]
        pattern_outcomes = entry[1]
        pattern_precision = measurements[pattern_abstraction]["P"]

        # skip patterns with no matches
        if pattern_precision == "unknown":
            continue

        # only add patterns to global group >=  than cuttoff
        if pattern_precision < cutoff:
            continue

        for extract_index, result in enumerate(pattern_outcomes):
            if extract_index not in group_results.keys():
                group_results[extract_index] = result

            if result == "TP" or result == "FP":
                group_results[extract_index] = result


    # calcluate the precision and recall
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for extract_index, group_result in group_results.items():
        if group_result == "TP":
            TP += 1
        if group_result == "TN":
            TN += 1
        if group_result == "FP":
            FP += 1
        if group_result == "FN":
            FN += 1

    print(f"group precision = {TP / (TP + FP)}")
    print(f"group recall = {TP / (TP + FN)}")

    with open(f"group_results_{working_folder}.json", "w") as f:
        json.dump(group_results, f, indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
