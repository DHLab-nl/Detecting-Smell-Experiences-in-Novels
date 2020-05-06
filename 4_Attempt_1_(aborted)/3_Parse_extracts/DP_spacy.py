"""Dep Parse extracts.txt, returning parsed_extract.txt

Example:
    $ python3 DP_spacy.py
"""
import json
import os

import spacy
from spacy import displacy


def main():

    # load spacy
    nlp = spacy.load("en_core_web_sm")

    # get parses
    with open("curated_extracts.json", "r") as f:
        extracts = json.load(f)

    # parse the sentences
    parses = []
    for url_code, book_extracts in extracts.items():

        for extract in book_extracts:
            doc = nlp(extract)

            parsed_sentence = ""  # ordered dict
            for token in doc:
                parsed_sentence += f"( {token.dep_} {token.text} {token.pos_} ) "
                # [child for child in token.children],

            parses.append(parsed_sentence)

    save_file = "parsed_extracts.txt"
    # remove existing save_file instances
    try:
        os.remove(save_file)
    except:
        pass

    # print parses to save_file
    with open("parsed_extracts.txt", "a") as f:
        for parsed_sentence in parses:
            f.write(parsed_sentence + "\n\n")


if __name__ == "__main__":
    main()
