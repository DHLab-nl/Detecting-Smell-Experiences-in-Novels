"""Count unique occurences of tags in annotations.json.
"""
import json

from collections import Counter, defaultdict


def main():

    with open("annotations.json", "r") as f:
        annotations = json.load(f)

    # annotations into a useful form
    save = {}  # {extract: [('tag', span), ...], ...}

    for set_key in annotations:
        for annotator in annotations[set_key]:
            for entry in annotations[set_key][annotator]:
                text = entry[0][1]

                if text not in save.keys():
                    save[text] = []
                save[text] += entry[0][2]  # += [(tag, span),...]

    # collect and print
    output = Counter()
    for text, items in save.items():
        for tag, span in items:
            output[tag] += 1

    print(output)

if __name__ == "__main__":
    main()
