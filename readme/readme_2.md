# Rank by high smell association keyword frequency

    Rank the English language texts in terms of high-smell association frequency, assumed indicative of number of smell experiences in each text.
    
## Navigate to folder
```
$cd 2_Rank_Catalogue
```

## Requires in folder:
* search_words.txt : i.e., a selection of high smell association keywords, indicative of text smell experience density

* catalogue.json : A **symbolic link** to ./1_Catalogue/catalogue.json


## Run...
```
$python3 search_word_frequency.py n
$python3 output_to_csv.py
```

## Args
    n (int): number of processes to run

## Output

1. Output from search_word_frequency.py\
A dictionary of texts, indexed by total keyword frequency\ 
found.json : {frequency: [(author, title, url_code,[list of keywords]), ...],...}

2. Output from output_to_csv.py\
found.csv : {freq, title, author, words, code} 
