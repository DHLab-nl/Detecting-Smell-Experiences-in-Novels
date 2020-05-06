"""
Example
    $ python3 check_sequences.py parsed_extracts.json
"""

import json
import re
import sys
from difflib import SequenceMatcher

import regex
import spacy
from tqdm import tqdm
from PATTERNS import patterns  # import user-defined patterns
from CHUNKS import chunks  # import user defined chunks


def convert_patterns(patterns):
    """Function to convert simplfied_patterns.json to python patterns. 
    Args:
        patterns (list):
        chuncks (dict):
    Returns:
        a list of python patterns
    """

    output = []
    pattern_as_string = []
    for pattern in patterns:
        pattern = convert_chunks(pattern)

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



def main(argv):

    # open parsed extracts
    with open(argv[0], "r") as f:
        extracts = json.load(f)

    converted_patterns = []
    for pattern, converted_pattern in zip(patterns, convert_patterns(patterns)):
        # print(converted_pattern + "\n\n")
        converted_patterns.append((pattern, converted_pattern))

    # print(converted_patterns[0])

    # iterate over extracts and patterns, groups matches and unmatched extracts
    matches = {}
    non_matched = []

    for counter, (book_code, extracts) in enumerate(extracts.items(), 1):
        print(f"\n\niterating over book {counter} extracts")
        for extract in tqdm(extracts):

            #remove anoying bits
            extract = extract.replace('punct_"_PUNCT', "")
            extract = extract.replace("punct_'_PUNCT", "")


            unmatched = True
            for simple_pattern, pattern in converted_patterns:
                mo = regex.match(".*" + pattern + ".*", extract)
                if mo:
                    unmatched = False
                    if simple_pattern in matches.keys():
                        matches[simple_pattern].append((book_code, extract))
                    else:
                        matches[simple_pattern] = [(book_code, extract)]
                    break  # stop looking for patterns
            if unmatched:
                non_matched.append(extract)

    # print matches
    for key, extracts in matches.items():
        print("-" * 50)
        print("\n" + key)
        print("-" * 50)
        for extract in extracts:
            print(extract)

    #
    print("\n\n")
    print("-" * 50)
    print("unmatched extracts")
    print("-" * 50)

    # print unmatched
    for unmatch in non_matched:
        print(unmatch + "\n\n")

    print(f"number matched = {sum([len(v) for k,v in matches.items()])}")
    print(f"number not matched = {len(non_matched)}")


if __name__ == "__main__":
    main(sys.argv[1:])
