"""count the number of author and books, english language only
"""
import json

def main():

    with open("catalogue.json", "r") as f:
        catalogue = json.load(f)

    book_counter = 0
    author_counter = 0
    authors = []
    for author, books in catalogue.items():
        author_counter += 1
        authors.append(author)
        for book, code in books:
            book_counter += 1

    for a in sorted(authors):
        print(a)
    print(f"total No. authors = {author_counter}")
    print(f"total No. authors = {book_counter}")


if __name__ == "__main__":
    main()
