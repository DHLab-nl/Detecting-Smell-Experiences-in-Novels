"""
Search.py, written by RJB 2020.

This script enables inspection of PG catalogue .json, output by catalogue.py

Example:
    $ python3 search_catalogue.py catalogue search_string

Args:
    catalogue (string): .json catalogue filename
    search_string (string): author, title, or book code

Returns:
    print full of partial matches of author, titles or book codes
"""

import json
import re
import sys


def retrieve_search(search_string, source):
    """Return a list of source entries that match search_string.

    Args:
        :search: a string string passed to re
        :source: a list of entries to search in
    """
    matches = []

    for item in source:
        mo = re.search(".*" + search_string.lower() + ".*", item.lower())
        if mo:
            matches.append(item)

    return matches


def main(argv):

    assert len(argv) == 2, "call python3 search.py catalogue search_string"

    catalogue = argv[0]
    search_string = argv[1]

    # retrieve the catalogue .json
    with open(catalogue, "r") as f:
        catalogue = json.load(f)  # {"author":[(title,code),..],..}

    authors = list(catalogue.keys())
    titles = [detail[0] for a, details in catalogue.items() for detail in details]
    codes = [detail[1] for a, details in catalogue.items() for detail in details]

    # return matching authors
    print("\n*Authors:*\n")
    print(retrieve_search(search_string, authors))

    # return matching titles
    print("*\nBook Titles*:\n")
    print(retrieve_search(search_string, titles))

    # return matching codes
    print("\n*Book codes*:\n")
    print(retrieve_search(search_string, codes))


if __name__ == "__main__":
    main(sys.argv[1:])
