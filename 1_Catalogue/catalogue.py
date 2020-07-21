"""
catalogue.py, written by RJB 2020

A script to extract the English Language books in the Project Gutenberg 
offline index to json {"author":[(title,code),..],..}

Example:
    $ python3 catalogue.py GUTINDEX.ALL

Returns:
    catalogue.json
"""

import sys
import json
import re
from tqdm import tqdm


class Catalogue:
    """A class to store book author, title and project Gut info.

    Attrbutes:
            books (dict): {"author":[(title,code),..],..}
    """

    def __init__(self):
        self.catalogue = {}

    def add_book(self, book):
        """Add book record to Catalogue object.

        Args:
            book: {author:[title, code]}
        """
        for author, details in book.items():

            # add author to self.catalogue if unknown
            if author not in self.catalogue.keys():
                self.catalogue[author] = []

            # add book to self.catalogue
            self.catalogue[author].append(details)


def main(argv):

    index = argv[0]

    # object for storing matching book entries
    catalogue = Catalogue()

    # counter - keep a record of No. books
    counter = 0

    # open project gutenberg offline index
    with open(index, "r") as f:
        book_to_save = False  # a signal whether to save book or not

        # iterate over each line
        book = None
        for line in tqdm(f):
            # identify book entries: isolate title, author, code
            # example entry: Knock at a Venture, by Eden Phillpotts      61549
            mo_entry = re.search(r"(.+),\sby\s([\w\s]+\w)\s\s+(\d+)", line)

            # if a match on current line, and not an audobook entry
            if mo_entry and not re.search(r"^(Audio:).*", line):

                # deal with previous entries, zero instruction to enter
                if book_to_save:
                    books = catalogue.add_book(book)
                    counter += 1

                # collect the new entry
                title = mo_entry.group(1)
                author = mo_entry.group(2)
                code = mo_entry.group(3)
                book = {author: (title, code)}

                # signal that there's a book for entry into the catalogue
                book_to_save = True

            # detect if English language
            mo_lang = re.search(r"\[\s*[L,l]anguage:*.*\]", line)
            mo_eng = re.search(r"\[\s*[L,l]anguage:*\s*([E,e]nglish\s*)+].*", line)
            if mo_lang and not mo_eng:
                book_to_save = False

    # output catalogue to json
    with open("catalogue.json", "w") as f:
        json.dump(catalogue.catalogue, f)

    print(f"total number of English books: {counter}")

if __name__ == "__main__":
    main(sys.argv[1:])
