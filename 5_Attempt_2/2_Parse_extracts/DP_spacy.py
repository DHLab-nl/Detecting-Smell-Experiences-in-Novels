"""Dep Parse extracts.txt, returning parsed_extract.txt

Example:
    $ python3 DP_spacy.py extracts.json
"""
import json
import os
import sys
from tqdm import tqdm

import spacy
from spacy import displacy


def main(argv):

    # load spacy
    nlp = spacy.load("en_core_web_sm")

    # get parses
    with open(argv[0], "r") as f:
        extracts = json.load(f)

    # parse the sentences
    parses = {}
    for url_code, book_extracts in tqdm(extracts.items()):
        parses[url_code] = []

        for extract in book_extracts:
            doc = nlp(extract)

            parsed_sentence = ""  # ordered dict
            for token in doc:
                parsed_sentence += f"{token.dep_}_{token.text}_{token.pos_} "

            parses[url_code].append(parsed_sentence)

    save_file = "parsed_extracts.txt"
    # remove existing save_file instances
    try:
        os.remove(save_file)
    except:
        pass

    # print parses to save_file
    with open("parsed_extracts.json", "w") as f:
        json.dump(parses,f)
    
    # with open("parsed_extracts.txt", "a") as f:
    #     for parse in parses:
    #         f.write(parse+"\n\n")



if __name__ == "__main__":
    main(sys.argv[1:])
