"""return a list of TN, TP, FP, FN outcomes for each extract by pattern

Example:
    $python3 pattern_targets.py  working_folder
    $python3 pattern_targets.py _aroma_NOUN+VERB

"""
import json
import multiprocessing
import os
import re
import sys
from tqdm import tqdm

import numpy as np
import regex
import spacy
# add libraries to path
sys.path.append(os.path.join(sys.path[0], "libraries"))
# add working folder to path
sys.path.append(os.path.join(sys.path[0], sys.argv[1]))

from CHUNKS import chunks
from pattern_abstraction import convert_patterns
from PATTERNS import extraction_patterns

def main(argv):


    # LOAD SPACY
    nlp = spacy.load("en_core_web_sm")

    working_folder = argv[0]

    with open("annotations.json") as f:
        annotations = json.load(f)

    results = []
    for s in tqdm(annotations):
        for annotator in annotations[s]:
            for entry in tqdm(annotations[s][annotator]):
                extract = entry[0][1]
                spans = entry[0][2]

                results.append((extract, spans, pattern_match(extract, nlp)))


    with open(f"results_{argv[0]}.json", "w") as f:
        json.dump(results, f, indent=4)


def pattern_match(text, nlp):

    text_parsed = ""
    doc = nlp(re.sub(r"\s+", " ", text.lower().replace("\n", " ")))
    for token in doc:
        text_parsed += f"{token.dep_}_{token.text}_{token.pos_} "

    matching = []
    for p in extraction_patterns:
        # print(p)

        # check for matches
        mo = regex.search(convert_patterns([p])[0], text_parsed)
        if mo:
            matching_features = [i for i in mo.groups() if len(i) > 0]
            if len(matching_features) == 2:
                matching.append((mo.groups(),p))

    return matching


if __name__ == "__main__":
    main(sys.argv[1:])
