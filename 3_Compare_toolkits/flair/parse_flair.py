"""Parse sample.txt, output parse_flair.txt of by-sentence (word, POS tag) pairs.
Example:
    $ python3 parse_spaCy.py

Note: uses nltk.tokenize.sent_tokenize to split into sentences
refer to https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md
"""
import json
import re
import timeit

import nltk
# https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md
from flair.data import Sentence
from flair.models import SequenceTagger
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm


def pos_tag(raw_text):
    """POS tag with flair. Sentence segmentation performed via nltk.

    Args:
        raw_text (str): A text string to be parsed.

    Returns: sentences object
    """
    # setup the libary
    tagger = SequenceTagger.load("pos-fast")

    # use nltk for segtence segmentation and tokenisation
    print("tokenising")
    sentences = []
    for sent in tqdm(sent_tokenize(raw_text)):
        sentences.append(Sentence(sent, use_tokenizer=True))  # uses segtok

    # predict pos tags
    print("tagging")
    tagger.predict(sentences)

    return sentences


def convert_tagging_format(sentences):
    """Convert sentence object to wanted format.

    Args:
        sentences where tagger.predict(sentences) has been run

    Return:
        a list of sentences, each sentence a list of token_tag strings
    """
    # assemble the relevant parse output features
    print("converting tagging format")
    output = []
    for sent_index, sent in enumerate(sentences):
        output.append([])
        sent_split = sent.to_tagged_string().split(" ")
        for i in range(0, len(sent_split), 2):
            token = sent_split[i]
            pos_tag = sent_split[i + 1].replace("<", "").replace(">", "")
            output[-1].append(token + "_" + pos_tag)

    return output


def main():

    # load raw document
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
    with open("parse_flair.json", "w") as f:
        json.dump(output, f)

    # # time the runtime
    # runs = 10
    # average_runtime = timeit.timeit(lambda: pos_tag(raw_text), number=runs) / 10
    # print(f"{runs} runs average run-time = {average_runtime}")


if __name__ == "__main__":
    main()
