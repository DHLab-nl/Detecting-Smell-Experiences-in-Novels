# run the following in a server
"""
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
-status_port 9000 -port 9000 -timeout 15000 &
"""

import json
import os
import sys

# see https://bbengfort.github.io/snippets/2018/06/22/corenlp-nltk-parses.html
# constituency (syntactic) parser
from nltk.parse.corenlp import CoreNLPParser
from tqdm import tqdm


def main(argv):
    """
    parse text via CoreNLParser
    """
    parser = CoreNLPParser()

    parse = next(parser.raw_parse(argv[0]))  # most likely parsing

    print(parse)
    print(parse.pretty_print())


if __name__ == "__main__":
    main(sys.argv[1:])
