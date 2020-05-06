import sys

import spacy
from nltk import Tree
from spacy import displacy


def main(argv):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(argv[0])

    print([to_nltk_tree(sent.root).pretty_print() for sent in doc.sents])


def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_, tok.dep_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)


if __name__ == "__main__":
    main(sys.argv[1:])
