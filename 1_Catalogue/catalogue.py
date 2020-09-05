"""
A script to extract the English Language books in the Project Gutenberg
offline index to json {"author":[(title,code),..],..}

Example:
    $ python3 catalogue.py GUTINDEX.ALL

Returns:
    catalogue.json
"""

import json
import re
import sys
from collections import defaultdict

import regex
from tqdm import tqdm


def main(argv):

    gutindex = argv[0]

    # iterate over project gutenberg offline gutindex, collect EL books
    with open(gutindex, "r", encoding="utf-8") as f:

        lines = f.read()

        # collect WHOLE PARAGRAPHS which start in the form, "Knock at a Venture, by Eden Phillpotts      61549"
        pattern = regex.compile(
            r".*?,\sby\s[\w\s]+\s+\d+.*?(?=.*?,\sby\s[\w\s]+\s+\d+)", re.DOTALL
        )
        paragraphs = regex.findall(pattern, lines)

        # extract (EL-only) book info from the paragraphs
        books = map(get_books_from_text, paragraphs)
        EL_books = list(filter(lambda x: x, books))  # non EL books listed as None

    # populate the json
    catalogue = defaultdict(list)
    for a, (t, c) in EL_books:
        catalogue[a] += [(t, c)]

    # output catalogue to json
    with open("catalogue.json", "w") as f:
        json.dump(catalogue, f, indent=4, ensure_ascii=False)

    print(f"total number of English books: {len(EL_books)}")


def get_books_from_text(line):
    """Extract and return (author, title, code) from text line. for EL books only.

    E.g., in the form, "Knock at a Venture, by Eden Phillpotts      61549"

    Args:
        line (str): text string passed

    Return: (author, title, code) or None if not EL
    """
    mo_entry = re.search(r"(.+),\sby\s([\w\s]+\w)\s\s+(\d+)", line)

    # matche object in the targetted form?
    if mo_entry and not re.search(r"^(Audio:).*", line):

        # detect if English language
        mo_lang = re.search(r"\[\s*[L,l]anguage:*.*\]", line)
        mo_eng = re.search(r"\[\s*[L,l]anguage:*\s*([E,e]nglish\s*)+].*", line)

        if not mo_lang or mo_eng:

            title = mo_entry.group(1)
            author = mo_entry.group(2)
            code = mo_entry.group(3)

            return (author, (title, code))
        else:
            return None
    else:
        return None


if __name__ == "__main__":
    main(sys.argv[1:])
