""" Return a .txt file with the n tokens with the greatest similarity to input word.
Example:
    get the 20 most similar words to dog (in terms of embeddings)
    $python dog 20
"""
import gensim.downloader as api
import sys

embeddings = api.load('word2vec-google-news-300')

# get ....
returned = []
for i in embeddings.most_similar(positive=sys.argv[1], topn=int(sys.argv[2])):
    returned.append(i)

# save to file
with open(f"results_{sys.argv[1]}_{sys.argv[2]}.txt", "w") as f:
    for r in returned:
        f.write(f"{r}\n")
