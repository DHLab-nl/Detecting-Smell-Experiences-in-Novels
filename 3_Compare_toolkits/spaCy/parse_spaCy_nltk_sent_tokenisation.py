"""Parse sample.txt, output parse_spaCy.txt of by-sentence (word, POS tag) pairs.

Text is initially tokenised into discrete sentences via nltk.tokenize.sent_tokenize

Example:
    $ python3 parse_spaCy.py
"""
import json
import timeit

import spacy
from nltk.tokenize import sent_tokenize


def pos_tag(raw_text):
    """POS tag with flair. Sentence segmentation performed via nltk.

    Args:
        raw_text (str): A text string to be parsed.

    Returns: sentences object
    """
    # setup the libary
    nlp = spacy.load("en")

    # return the parse of raw_doc
    sentences = [nlp(sent) for sent in sent_tokenize(raw_text)]

    return sentences


def convert_tagging_format(sentences):
    """Convert sentences object to wanted format.

    Args:
        sentences where tagger.predict(sentences) has been run

    Return:
        a list of sentences, each sentence a list of token_tag strings
    """
    # assemble the relevant parse output features
    output = []
    for sent_index, sent in enumerate(sentences):
        output.append([])
        for token in sent:
            if token.pos_ != "SPACE":
                output[-1].append(token.text + "_" + token.pos_)

    return output


def main():

    print("Loading the raw text")
    with open("pg19337.txt", "r") as f:
        raw_text = f.read()

    # predict pos tags
    print("Predicting POS tags")
    sentences = pos_tag(raw_text)

    # format
    print("Convert POS tag format")
    output = convert_tagging_format(sentences)

    # save as a json
    with open("parse_spaCy.json", "w") as f:
        json.dump(output, f)

    # # time the runtime
    # runs = 10
    # average_runtime = timeit.timeit(lambda: parse(raw_text), number=runs) / runs
    # print(f"{runs} runs average run-time = {average_runtime}")


if __name__ == "__main__":
    main()
