""" Output to terminal the 100 most similar words (in embedding repr) to 'smell'

Example:
    $python3 embeddings.py
"""
import gensim.downloader as api

wv = api.load('word2vec-google-news-300')

with open("search_words.txt", "r") as f:
    search_words = [w.strip("\n") for w in f.readlines()]

print(search_words)
#print the topn vectors most similar to ....
vector = ["smell"]
for i in wv.most_similar(positive=vector, topn=100): print(i)
