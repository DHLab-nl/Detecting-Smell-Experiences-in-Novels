# Catalogue all English language Project Gutenberg resources
    I.e., collect all texts where specified as English, or unspecified (English default)
    
## Navigate to folder
```
$ cd 1_Catalogue
```

## Requires in folder:
* GUTINDEX.ALL from https://www.gutenberg.org/dirs/GUTINDEX.ALL

## Run...
```
$ python3 catalogue.py GUTINDEX.ALL
```

## Output
catalogue.json : {"Author":[("book title"), ...], ...}

