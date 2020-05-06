"""
Example
    $ python3 check_sequences.py parsed_extracts.json
"""

import json
import re
import sys
from difflib import SequenceMatcher

import spacy


def convert_patterns(patterns):

    output = []
    pattern_as_string = []
    for pattern in patterns:
        pattern = convert_chunks(pattern)
        print(pattern)

        python_pattern = []

        # setup curly brace handling pattern repetitions
        python_pattern = []

        # convert each token to a python pattern
        blocks = [
            t
            for t in re.split(r"({|\[|}\*|}\+|\]\*|\]\+|\])|\s+", pattern)
            if t is not "" and t is not None
        ]

        # iterate over blocks
        for block_index, block in enumerate(blocks):
            print(block)

            # reset for handling block *, +
            zero_or_more, one_or_more = False, False

            # handle brackets
            if block == "{":
                python_pattern.append("(?:")
                continue
            elif block == "}*":
                python_pattern.append(")*")
                continue
            elif block == "}+":
                python_pattern.append(")+")
                continue
            elif block == "[":
                python_pattern.append("(")
                continue
            elif block == "]":
                python_pattern.append(")")
                continue
            elif block == "]*":
                python_pattern.append(")*")
                continue
            elif block == "]+":
                python_pattern.append(")+")
                continue

            # handle *, + operators (record and remove)
            if block[-1] == "*":
                block = block[:-1]
                zero_or_more = True
            if block[-1] == "+":
                block = block[:-1]
                one_or_more = True

            # split into parse components and process
            dep, text, pos = block.split("_")
            if dep == "":
                dep = "\S+"
            if text == "":
                text = "\S+"
            if pos == "":
                pos = "\S+"

            # process | in dep, text or pos
            if "|" in dep:
                dep = "(?:" + dep + ")"
            if "|" in text:
                text = "(?:" + text + ")"
            if "|" in pos:
                pos = "(?:" + pos + ")"

            # implement *, +
            if zero_or_more:
                token_python = "(?:" + dep + "_" + text + "_" + pos + ")*"
            elif one_or_more:
                token_python = "(?:" + dep + "_" + text + "_" + pos + ")+"
            else:
                token_python = dep + "_" + text + "_" + pos

            python_pattern.append(token_python)

            # reset
            zero_or_more, one_or_more = False, False

        # append to output as string
        pattern_as_string = ""
        last_term = None
        for term in python_pattern:
            if last_term is None:
                pattern_as_string += term
            elif last_term in ["(", "(?:", "{"]:
                pattern_as_string += term
            elif term in ["}*", "}+", ")", ")*", ")+"]:
                pattern_as_string += term
            else:
                pattern_as_string += "\s*" + term
            last_term = term

        output.append(pattern_as_string)

    return output


def convert_chunks(pattern):
    """Expand chuncks, e.g. <nouns> in the pattern, as defined in chunks {}.
       Capable of handling nested chunks
    Args:
        pattern (str): simplified sentence pattern
    """
    blocks = []
    for block in re.split(r"\s+|(}\*|}\+|}|\]|{|\[)", pattern):

        if block is None or block == "":
            continue

        if block[0] == "<":
            if block[-1] == "*":
                blocks.append("{" + chunks[block[:-1]] + "}*")
            else:
                blocks.append(chunks[block])
        else:
            blocks.append(block)

    # append to output as string
    pattern_as_string = ""
    last_term = None
    for term in blocks:
        if last_term is None:
            pattern_as_string += term
        elif last_term in ["{"]:
            pattern_as_string += term
        elif term in ["}*", "}+"]:
            pattern_as_string += term
        else:
            pattern_as_string += " " + term
        last_term = term

    if "<" in pattern_as_string:
        return convert_chunks(pattern_as_string) 
    else:
        return pattern_as_string

# later can reference earlier only
chunks = {
    "<adj>": "__ADJ+ {_and|,|or_ __ADJ}*",
    # the tall, dark and handsome
    #
    "<adv>": "__ADV+ {_and|,|or_ __ADV}*",
    #
    "<verb>": "<adv>* __VERB <adv>* {_and|,|or_ <adv>* __VERB <adv>*}*",
    #loadly singing, laughing and dancing wildly
    #
    "<prep>": "prep__ det__*",
    #with the , of the , in the, of
    #
    "<noun>": "det__* <adj>* compound__* _-_* __NOUN {_and|,|or_* det__* <adj>* compound__* _-_* __NOUN}*",
    #green, mottled tree-bark and pale roots of the tree
    #
    "<subj>": "det__* <adj>* compound__* _-_* subj__ <prep>* {_and|,|or_* det__* <adj>* compound__* _-_* conj__}*"
}


patterns = [
    "_scent_VERB <subj> _with_ <noun>",
    #
    "<subj> _reeks|smells|pongs_ __VERB <adv>*",
    #
    "<verb> _to_ <adv>* _reek|pong|smell_VERB <adv>*"
    #
]


def main(argv):

    # open parsed text
    with open(argv[0], "r") as f:
        extracts = json.load(f)

    for pattern in convert_patterns(patterns):
        print(pattern + "\n\n")

    # # init dict to store pattern matches
    # matches = {}
    # for p in patterns:
    #     matches[p] = []

    # # store extracts with no matches
    # no_match = []

    # # iterate over extracts/ patterns
    # total_matched = 0
    # for extract in extracts:
    #     for pattern in patterns:
    #         mo = re.match(f".*{pattern}.*", extract)
    #         if mo is not None:
    #             total_matched += 1
    #             matches[pattern].append(extract)
    #         else:
    #             no_match.append(extract)

    # # print unmatched extracts
    # for pattern in no_match:
    #     print(pattern + "\n")

    # print(f"total matched = {total_matched}")


if __name__ == "__main__":
    main(sys.argv[1:])
