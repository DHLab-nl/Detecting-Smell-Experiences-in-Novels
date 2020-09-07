"""Count unique occurences of tags in annotations.json.
"""
import json

from collections import Counter


def main():

    with open("annotations.json", "r") as f:
        annotations = json.load(f)

    # annotations into a useful form
    save = {}  # {extract: [('tag', span), ...], ...}

    for set_key in annotations:
        for annotator in annotations[set_key]:
            for entry in annotations[set_key][annotator]:
                text = entry[0][1]
                save[text] = []

                tags = list(set([(tag, span) for tag, span in entry[0][2]]))
                save[text] += tags

    # collect and print
    output = Counter()
    for text, items in save.items():
        for tag, span in items:
            output[tag] += 1

    print(output)




if __name__ == "__main__":
    main()
