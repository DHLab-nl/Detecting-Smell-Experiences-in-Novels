"""Examine the book spread by author initial.
"""
import json
from collections import Counter

import regex


def main():

    with open("catalogue.json", "r") as f:
        catalogue = json.load(f)

    authors_count = Counter()
    initial_count = Counter()

    for author, books in catalogue.items():
        authors_count[author] += len(books)
        initial_count[author[0]] += len(books)

    for author in sorted(authors_count):
        print(f"{author}: {authors_count[author]}")

    for initial in initial_count:
        print(f"{initial}: {initial_count[initial]}")


if __name__ == "__main__":
    main()
