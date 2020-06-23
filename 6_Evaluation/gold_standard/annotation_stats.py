"""Get annotation stastistics for report writing
"""

import json

def main():
    with open("annotations.json", "r") as f:
        annotations = json.load(f)


    # ASSEMBLE the annotations into a more usable form
    counter = {}
    # {set: {annotator:{extract : (extract tags), ...}, ...}, ... }
    for set in annotations.keys():
        counter[set] = {}
        for annotator in annotations[set].keys():
            counter[set][annotator] = {}
            for entry in annotations[set][annotator]:
                extract = entry[0][0]
                tags = [span[0] for span in entry[0][1]]

                counter[set][annotator][extract] = tags

    # total number of extracts
    extracts = 0
    for set_name, set in counter.items():
        for annotator in set:
            extracts += len(set[annotator].keys())
            break  # consider first annotator only

    print(f"total number of extracts: {extracts}")

    # total number of extracts tagged 'd', 'o', 'd' or 'o', 'v', 'v' and 'd' or 'o'
    d = 0
    o = 0
    d_or_o = 0
    v = 0
    v_and_d_or_o = 0
    s = 0
    s_and_d_or_o = 0
    v_and_s = 0
    for set_name, set in counter.items():
        for annotator in set:
            for extract, tags in set[annotator].items():
                if 'd' in tags:
                    d += 1
                if 'o' in tags:
                    o += 1
                if 'd' in tags or 'o' in tags:
                    d_or_o += 1
                if 'v' in tags:
                    v += 1
                if 'v' in tags and ('d' in tags or 'o' in tags):
                    v_and_d_or_o += 1
                if 's' in tags:
                    s += 1
                if 's' in tags and ('d' in tags or 'o' in tags):
                    s_and_d_or_o += 1
                if 'v' in tags and 's' in tags:
                    v_and_s += 1

            break  # consider first annotator only

    print(f"total number of 'd': {d}")
    print(f"total number of 'o': {o}")
    print(f"total number of 'd or o': {d_or_o}")
    print(f"total number of 'v': {v}")
    print(f"total number of 'v' with 'd' or 'o': {v_and_d_or_o}")
    print(f"total number of 's': {s}")
    print(f"total number of 's' with 'd' or 'o': {s_and_d_or_o}")
    print(f"total number of 'v' and 's': {v_and_s}")


if __name__ == "__main__":
    main()
