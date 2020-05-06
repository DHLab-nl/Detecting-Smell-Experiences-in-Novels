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


##simplify the patterns further with noun chunks, for first stage of conversion
# verb_chunk-> __ADV* __VERB
# noun_chuck -> det__* __ADJ* __NOUN

chunks = {
    #
    "<nouns>": "det__* __ADJ* {_and|,_* __ADJ*}* [__NOUN] {_and|,_* __ADJ* __NOUN}*",
}


patterns = [
    # I will scent 'em with best vanilla
    "_scent|smell_VERB [dobj__] _with_ [det__* __ADJ* pobj__] {_and|,_ [det__* __ADJ* __NOUN]}*",
    # they are starting to smell bad
    # "[nsubj__]  __ADV* __VERB _to_ __ADV* _smell_VERB [__ADV* __ADJ*] {_and_ __ADV* __ADJ*}*",
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
