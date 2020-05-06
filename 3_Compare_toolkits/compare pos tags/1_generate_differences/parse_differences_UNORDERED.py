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

    # compare by sentence parses (as unordered sets)
    differences = []
    for sent_index in range(len(parses[0])):

        # collect current sentence for each of flair, spaCy and stanza
        sentence_flair = [token + "_" + tag for token, tag in parses[0][sent_index]]
        sentence_spaCy = [token + "_" + tag for token, tag in parses[1][sent_index]]
        sentence_stanza = [token + "_" + tag for token, tag in parses[2][sent_index]]
        #
        set_flair = set(sentence_flair)
        set_spaCy = set(sentence_spaCy)
        set_stanza = set(sentence_stanza)

        # identify differences (union - intersection) between spaCy and flair
        diff_spaCy = set_spaCy - set_flair  # set_flair.union(set_spaCy) - set_flair.intersection(set_spaCy)
        diff_stanza = set_stanza - set_flair  # set_flair.union(set_stanza) - set_flair.intersection(set_stanza)
        diff_stanza_spaCy = diff_spaCy - diff_stanza

        if not any(diff_spaCy):
            diff_spaCy = ""
        if not any(diff_stanza):
            diff_stanza = ""
        if not any(diff_stanza_spaCy):
            diff_stanza_spaCy = ""

        # record differences
        differences.append(
            [
                sentence_flair,
                len(sentence_flair),
                diff_spaCy,
                len(sentence_spaCy),
                diff_stanza,
                len(sentence_stanza),
                diff_stanza_spaCy
            ]
        )

        

    # save differences to csv
    df = pd.DataFrame(
        differences,
        columns=[
            "(flair-tagged) sentence",
            "",
            "spaCy - flair",
            "",
            "stanza - flair",
            "",
            "stanza - spaCy"
        ],
    )
    df.to_csv("parse_differences.csv", sep=";")

if __name__ == "__main__":
    main()
