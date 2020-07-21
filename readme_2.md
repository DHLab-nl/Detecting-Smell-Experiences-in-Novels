# Rank by high smell association keyword frequency

## Requires in folder:
* search_words.txt
i.e., a selection of high smell association keywords, indicative of text smell experience density

* catalogue.json
A symbolic link to /1_Catalogue/catalogue.json


## Run...
```
$cd 2_Rank_Catalogue
$python3 search_word_frequency.py
$python3 output_to_csv.py
```

## Output

1. A dictionary of texts, indexed by total keyword frequency
{frequency: [(author, title, url_code,[list of keywords]), ...],...}

2. A csv of texts, ranked by high smell association frequency keyword
