"""Return a list of lexicon entry pairs, matched by the any and all
implementation extraction patterns.

Example:
    $python3 lexicon_matches.py  working_folder
    $python3 lexicon_matches.py _aroma_NOUN+VERB

"""
import json
import os
import re
import sys

import regex
import spacy
from tqdm import tqdm

# add libraries to path
sys.path.append(os.path.join(sys.path[0], "libraries"))
# add working folder to path
sys.path.append(os.path.join(sys.path[0], sys.argv[1]))

from CHUNKS import chunks
from pattern_abstraction import convert_patterns
from PATTERNS import extraction_patterns


def main(argv):

    # Args
    working_folder = argv[0]

    # Load spacy
    nlp = spacy.load("en_core_web_sm")

    with open("annotations.json") as f:
        annotations = json.load(f)

    # assemble a list of lexicon pair entries, from all implementation patterns
    results = []
    for s in tqdm(annotations):
        for annotator in annotations[s]:
            for entry in annotations[s][annotator]:
                extract = entry[0][1]
                spans = entry[0][2]

                results.append((extract, spans, pattern_match(extract, nlp)))

    # results = [("amod_fresh_ADJ", "pobj_bouquet_NOUN"), ...]

    with open(f"results_{working_folder}.json", "w") as f:
        json.dump(results, f, indent=4)


def pattern_match(text, nlp):
    """
    Args:
        text (str): An unparsed text extract
        nlp: for spacy syntactic parsing

    Returns: [("amod_fresh_ADJ", "pobj_bouquet_NOUN"), ...]
    """

    # Parse text
    text_parsed = ""
    doc = nlp(re.sub(r"\s+", " ", text.lower().replace("\n", " ")))
    for token in doc:
        text_parsed += f"{token.dep_}_{token.text}_{token.pos_} "
    # "subj_wine_NOUN cc_and_CCONJ ..."

    # Iterate through all extraction patters (working folder specific), and
    # return tassemble a list of lexicon entry pairs for matching patterns.
    matching = []
    for p in extraction_patterns:

        mo = regex.search(convert_patterns([p])[0], text_parsed)
        if mo:
            matching_features = [i for i in mo.groups() if len(i) > 0]
            if len(matching_features) == 2:
                matching.append((mo.groups(), p))
    # matching = [("amod_fresh_ADJ", "pobj_bouquet_NOUN"), ...]

    return matching


if __name__ == "__main__":
    main(sys.argv[1:])
