"""Parse sample.txt, output parse_stanza.json of by-sentence (word, POS tag) pairs.

Text is initially tokenised into discrete sentences via nltk.tokenize.sent_tokenize

Example: 
    $ python3 parse_stanza.py

Note: uses the nltk tokeniser to split into sentences, prior to passing to stanza

stanza reference
# https://stanfordnlp.github.io/stanza/installation_usage.html#getting-started
"""
import json
import timeit

import stanza
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

def pos_tag(raw_text):
    """POS tag with stanza. Sentence segmentation performed via nltk.

    Args:
        raw_text (str): A text string to be parsed.

    Returns: sentences object
    """

    # library config
    config = {"lang": "en", "processors": "tokenize,mwt,pos"}
    nlp = stanza.Pipeline(**config)

    # return parse of raw_doc
    processed = []
    for sentence in sent_tokenize(raw_text):
        processed.append(nlp(sentence))

    return processed


def convert_tagging_format(processed):
    """Format.
    """
    # assemble relevant parse output into output
    output = []
    for sentence in processed:
        for doc in sentence.sentences:
            for token in doc.words:
                output.append(token.text + "_" + token.upos)

    return output


def main():

    # load raw text
    print("Loading the raw text")
    with open("pg19337.txt", "r") as f:
        raw_text = f.read()

    # parse raw text, output a
    print("Predicting POS tags")
    processed = pos_tag(raw_text)

    # format
    print("Convert POS tag format")
    output = convert_tagging_format(processed)

    # save as a json
    with open("parse_stanza.json", "w") as f:
        json.dump(output, f)

    # # time the runtime
    # runs = 10
    # average_runtime = timeit.timeit(lambda: parse(raw_text), number=runs) / runs
    # print(f"{runs} runs average run-time = {average_runtime}")


if __name__ == "__main__":
    main()
