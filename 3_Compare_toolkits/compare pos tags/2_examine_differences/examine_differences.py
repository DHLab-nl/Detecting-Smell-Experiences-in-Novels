"""Read in par e_differnces.csv and .... 

Example:
    $ python3 examine_differences.py
"""

import json
import re
from collections import Counter

import numpy as np
import pandas as pd


def main():

    # import differences form csv
    df = pd.read_csv("parse_differences.csv", sep=";")
    spaCy_flair_raw = df["spaCy - flair"]
    stanza_flair_raw = df["stanza - flair"]
    stanza_spaCy_raw = df["spaCy - stanza"]

    # collect spaCy - flair differnces
    spaCy_dict = Counter()
    for i in spaCy_flair_raw.to_list():
        try:
            tokens = re.split(
                ", ", i.replace("{", "").replace("}", "").replace("'", "")
            )
            for token in tokens:
                spaCy_dict[token] += 1

        except:
            pass

    # output to json
    with open("spaCy_differences.json", "w") as f:
        json.dump(spaCy_dict, f)

    # collect stanza - flair differences
    stanza_dict = Counter()
    for i in stanza_flair_raw.to_list():
        try:
            tokens = re.split(
                ", ", i.replace("{", "").replace("}", "").replace("'", "")
            )
            for token in tokens:
                stanza_dict[token] += 1

        except:
            pass

    # output to json
    with open("stanza_differences.json", "w") as f:
        json.dump(stanza_dict, f)


    # collect stanza - spaCy differences
    stanza_spaCy_dict = Counter()
    for i in stanza_spaCy_raw.to_list():
        try:
            tokens = re.split(
                ", ", i.replace("{", "").replace("}", "").replace("'", "")
            )
            for token in tokens:
                stanza_spaCy_dict[token] += 1

        except:
            pass

    # output to json
    with open("stanza_differences.json", "w") as f:
        json.dump(stanza_spaCy_dict, f)

    #
    # print the top 20
    #
    print("\nspaCy - flair:\n\n")
    print(spaCy_dict.most_common(50))

    #
    # print the top 20
    #
    print("\nstanza - flair:\n\n")
    print(stanza_dict.most_common(50))

    #
    # print the top 20
    #
    print("\nstanza - spaCy:\n\n")
    print(stanza_spaCy_dict.most_common(50))

if __name__ == "__main__":
    main()
