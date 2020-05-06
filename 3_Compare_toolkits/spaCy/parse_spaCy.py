"""Parse sample.txt, output parse_spaCy.txt of by-sentence (word, POS tag) pairs.
Example:
    $ python3 parse_spaCy.py

Note: uses in-built tokeniser
"""
import json
import timeit

import spacy


def pos_tag(raw_text):
    """POS tag with flair. Sentence segmentation performed via nltk.

    Args:
        raw_text (str): A text string to be parsed.

    Returns: sentences object
    """
    # setup the libary
    nlp = spacy.load("en")

    # return the parse of raw_doc
    doc = nlp(raw_text)

    return doc


def convert_tagging_format(doc):
    """Convert doc object to wanted format.

    Args:
        doc: spacy processed text

    Return:
        a list of sentences, each sentence a list of token_tag strings
    """

    # assemble the relevant parse output features
    output = []
    for sent_index, sent in enumerate(doc.sents):
        output.append([])
        for token in sent:
            if token.pos_ != "SPACE":
                output[-1].append((token.text + "_" + token.pos_))

    return output


def main():

    with open("pg19337.txt", "r") as f:
        raw_text = f.read()

    # predict pos tags
    print("Predicting POS tags")
    doc = pos_tag(raw_text)

    # format
    print("Convert POS tag format")
    output = convert_tagging_format(doc)

    # save as a json
    with open("parse_spaCy.json", "w") as f:
        json.dump(output, f)

    # # time the runtime
    # runs = 10
    # average_runtime = timeit.timeit(lambda: pos_tag(raw_text), number=runs) / runs
    # print(f"{runs} runs average run-time = {average_runtime}")


if __name__ == "__main__":
    main()
