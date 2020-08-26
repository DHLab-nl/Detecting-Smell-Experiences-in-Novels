"""Check number of sentence overlaps in /datasets.
"""
import os


def main():

    datasets = list(map(get_extracts, os.listdir("./samples")))
    # [book_0_sentence_set,...]

    # compare every dataset pairs
    for i in range(len(datasets)):
        for j in range(i + 1, len(datasets)):
            print(
                datasets[i][0],
                datasets[j][0],
                len(datasets[i][1].intersection(datasets[j][1])),
            )


def get_extracts(file):
    """Return a set of sentences, wrt. file name arg."""

    filename = os.fsdecode(file)
    with open("./samples/" + filename, "r") as f:
        dataset = map(
            lambda l: l.strip("\n"), filter(lambda l: l != "\n", f.readlines())
        )

    return (file, set(dataset))


if __name__ == "__main__":
    main()
