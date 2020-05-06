"""Analyse the difference in parse_flair.json, parse_spaCy.json and parse_stanza.json.

Example:
    $ python3 analyse_parse_differences.py

Returns:
    parse_differences.csv: a csv of parse listed differences wrt. flair parse
"""
import json

import pandas as pd
from tqdm import tqdm


def main():

    # load the parses
    parses = []
    for file in ["parse_flair.json", "parse_spaCy.json", "parse_stanza.json"]:
        with open(file, "r") as f:
            parses.append(json.load(f))

    # compare by sentence parses
    differences = []
    for sent_index in range(len(parses[0])):

        # collect current sentence for each of flair, spaCy and stanza
        sentence_flair = parses[0][sent_index]
        sentence_spaCy = parses[1][sent_index]
        sentence_stanza = parses[2][sent_index]

        # identify differences between spaCy and flair
        diff_spaCy = []
        for f, s in zip(sentence_flair, sentence_spaCy):
            if f != s:
                diff_spaCy.append(s)

        diff_stanza = []
        for f, s in zip(sentence_flair, sentence_stanza):
            if f != s:
                diff_stanza.append(s)

        # record differences
        differences.append(
            [
                sentence_flair,
                diff_spaCy,
                diff_stanza,
            ]
        )


    # save differences to csv
    df = pd.DataFrame(differences, columns=["sentence", "spaCy difference", "stanza difference"])
    df.to_csv("parse_differences.csv", sep=";")


if __name__ == "__main__":
    main()
