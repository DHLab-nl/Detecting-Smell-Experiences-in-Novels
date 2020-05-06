"""Sort literature.csv. Can also be used for non-literature.csv and repetitions.csv

Example: sort by author
    $ python3 sorted.py literature.csv author

Example: sort by freq (in descending order)
    $ python3 sorted.py literature.csv freq.
"""

import sys

import pandas as pd


def main(argv):

    # handle command line arguments
    assert "author" in argv or "freq." in argv, "2 command line arguments required"

    df = pd.read_csv("literature.csv")

    if argv[1] == "author":
        df_new = df.iloc[:, 1:].sort_values(by=["author", "title"]).reset_index(drop=True)
    elif argv[1] == "freq.":
        df_new = df.iloc[:, 1:].sort_values(by=["freq."], ascending=False).reset_index(drop=True)

    df_new.to_csv(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
