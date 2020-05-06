import sys

import spacy
from spacy import displacy

from Linked_List import LinkedList, Node

# what am i trying to do?
# 1) write a script identified the structure of a sentence


def main(argv):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(argv[0])

    for token in doc:
        print(token.dep_, token.text+"_"+token.pos_)#, [child for child in token.children])

    displacy.serve(doc, style="dep")

if __name__ == "__main__":
    main(sys.argv[1:])
