"""quick script how many sentences in the harvest set?
"""
import os

import pandas as pd
import wget
from nltk.tokenize import sent_tokenize
from tqdm import tqdm


def main():

    df = pd.read_csv("harvesting.csv")

    sentence_count = []
    for index, row in df.iterrows():
        print(index)
        code = row["code"]
        try:
            file_name = f"{code}.txt"
            if os.path.exists(f"./books/{file_name}"):
                pass
            else:
                url = f"https://www.gutenberg.org/files/{code}/{file_name}"
                wget.download(url, bar=None, out=f"./books/{file_name}")
        except:
            # failed? try to find with file suffix 1-10
            for i in range(0, 11):
                try:
                    file_name = f"{code}-{i}.txt"
                    url = f"https://www.gutenberg.org/files/{code}/{file_name}"
                    if os.path.exists(f"./books/{file_name}"):
                        break
                    else:
                        wget.download(url, bar=None, out=f"./books/{file_name}")
                        break
                except:
                    pass

        with open(f"./books/{file_name}", "r") as f:
            book = f.read()

        sentence_count.append(sum([1 for s in sent_tokenize(book)]))

    df["sentence_count"] = sentence_count
    df["density"] = df["freq."] / df["sentence_count"]

    df.to_csv("modified.csv", sep=",")


if __name__ == "__main__":
    main()
