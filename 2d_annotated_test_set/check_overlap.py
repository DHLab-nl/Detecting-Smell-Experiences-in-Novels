import os


def main():
    datasets = []

    for file in os.listdir("./samples"):
        filename = os.fsdecode(file)
        with open("./samples/" + filename, "r") as f:
            dataset = set([line.strip("\n") for line in f.readlines() if line != "\n"])
        datasets.append(dataset)

    for i in range(len(datasets)):
        for j in range(i + 1, len(datasets)):
            print(i, j, len(datasets[i].intersection(datasets[j])))

    print(1, 1, len(datasets[i].intersection(datasets[j])))


if __name__ == "__main__":
    main()
