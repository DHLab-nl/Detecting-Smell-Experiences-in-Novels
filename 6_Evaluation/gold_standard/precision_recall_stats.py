"""A script which does 2 things, wrt. a specified working_folder, i.e., implementation.

    1) Calculate by-pattern recall & precision from TP, TN, FP wrt.
       "outcomes_{working_folder}.json".

       output file : "measures_by_pattern_{working_folder}.json"
       This is irrespective of threshold command line arg

    2) Determine the group prediction outcomes, where patterns whose individual
       precision about the threshold are included in the group prediction.

        output file "group_results_{working_folder}.json"

        How group prediction is assessed....
        * An extract is either positive (a smell experience) or negative (not)
        * The group predicts positive if at least one pattern within the group,
          matches. Otherwise, with no matches, the group predicts negative
        * if positive, the pattern outcomes must be either TP, FN.
            * Thus, if a single pattern in the group is TP, since text is deemed
            positive based on a single match or more, the group prediction is
            TP. otherwise the group prediction is FN.
            * Similarly, is a sentence is not a smell experience, a pattern is
            either TN, or FP. Thus, if a single pattern is FP, the group
            prediction is FP. Otherwise TN.


Calculate the precision and recall by pattern.
   output a json file

Example:
    $python3 precision_recall_stats.py working_folder cutoff
    $python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.90

working_folder (string): folder containing PATTERNS.py of interest

Returns:
    measures_by_pattern_{working_folder}.json
    (terminal) precision & recall value for global group, for patterns p >= cutoff
"""
import json
import sys
from collections import defaultdict


def get_pattern_stats(p_outcomes):
    """
    Args:
        P_outcomes (list): (pattern_abstraction, [**])
    """
    pattern_abstraction, outcomes = p_outcomes

    TP = outcomes.count("TP")
    FP = outcomes.count("FP")
    FN = outcomes.count("FN")

    if TP + FP == 0:  # No extract matches for which to grade performance
        precision = "unknown"
        recall = "unknown"
    else:
        epsilon = 1e-6
        precision = TP / (TP + FP + epsilon)
        recall = TP / (TP + FN + epsilon)

    return (pattern_abstraction, precision, recall)


def get_group_predictions(patterns, outcomes_d):
    """
    patterns (list): [pattern_abstraction,...] iter
    outcomes_d (dict): {pattern_abstraction:[**]}

    Returns: {extract_index:group_outcomes}
    """
    num_sentences = len(list(outcomes_d.items())[0][1])

    group_outcomes = defaultdict()
    for index in range(num_sentences):
        for pattern_abstraction, outcomes in outcomes_d.items():

            if pattern_abstraction in patterns:
                pattern_outcome = outcomes[index]

                # case: we have a pattern match
                if pattern_outcome == "TP":
                    group_outcomes[str(index)] = "TP"
                    break  # group pred. is pos with single match ... stop looking
                elif pattern_outcome == "FP":
                    group_outcomes[str(index)] = "FP"
                    break

                # case: we don't have a match
                group_outcomes[str(index)] = pattern_outcome

    return group_outcomes


def main(argv):

    # CL args
    working_folder = argv[0]
    cutoff = float(argv[1])

    with open(f"./prediction_labels_patterns/prediction_labels_{working_folder}.json", "r") as f:
        outcomes = json.load(f)
        # [ (pattern_abstraction, [**]),..]
        # where [**] is list of by-extract TP/FN/TN/FP labels

    # ------
    # 1. Get the by-pattern precision and recall stats
    # ------

    # Get by pattern precision, recall stats
    pattern_stats = list(map(get_pattern_stats, outcomes))
    # [(pattern_abstraction, precision, recall),...]

    # determine the by-pattern recall and precision
    measurements = defaultdict()
    for a, p, r in pattern_stats:
        measurements[a] = {"P": p, "R": r}
    # measurements = {"pattern":{"P":0.4 , "R":0.2}}

    with open(f"./precision_recall_stats_patterns/stats_by_pattern_{working_folder}.json", "w") as f:
        json.dump(measurements, f, indent=4)

    # ------
    # 2. Group prediction results, wrt cutoff
    # ------

    # Collect those patterns whose precision >=  cutoff
    filtered_stats = filter(
        lambda i: i[1] >= cutoff, filter(lambda s: s[1] != "unknown", pattern_stats)
    )
    # [(pattern_abstraction, precision, recall),...] iter
    filtered_patterns = list(map(lambda i: i[0], filtered_stats))
    # [pattern_abstraction,...]

    # Get a dict of outcomes
    outcomes_d = dict(outcomes)
    # [pattern_abstraction:[**]]

    group_outcomes = get_group_predictions(filtered_patterns, outcomes_d)
    # {extract_index:group_prediction}

    # save the group prediction labels
    with open(f"./prediction_labels_group/group_labels_{working_folder}_{argv[1]}.json", "w") as f:
        json.dump(group_outcomes, f, indent=4)

    # ------
    # 2b: calculate the precision and recall of the group predicions
    # ------

    outcomes = list(zip(*group_outcomes.items()))[1]
    # [TP, TP, FN,...]

    name, precision_group, recall_group = get_pattern_stats(("group", outcomes))

    print(f"group precision = {precision_group}")
    print(f"group recall = {recall_group}")


if __name__ == "__main__":
    main(sys.argv[1:])
