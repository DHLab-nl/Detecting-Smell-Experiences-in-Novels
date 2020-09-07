# Evaluation of pattern lexicon feature targeting

## Navigate to 
```
cd 6_Evaluation/annotations_subset_a,v,n
```

## Assemble annotation set specifically tagging adjectives, nouns and verbs referenced in textual smell experiences

### Navigate to 
```
cd 6_Evaluation/annotations_subset_a,v,n/sets
```

### Run
```
$python3 get_annotations.py 
```

## Get a compiled json of annotation tags and pattern object extracts for each pattern in an implementation

### Navigate to ...
```
cd 6_Evaluation/annotations_subset_a,v,n
```

### Requires in folder
* annotations.json - a symbolic link to ./sets/annotations.json
* /_aroma_NOUN+VERB, containing PATTERNS.py consisting of extraction patterns
* /_aroma_NOUN+ADJ, containing PATTERNS.py consisting of extraction patterns

### Run
```
python3 lexicon_matches.py _aroma_NOUN+VERB
python3 lexicon_matches.py _aroma_NOUN+ADJ
```

### Returns
* results__aroma_NOUN+ADJ.json
* results__aroma_NOUN+VERB.json

TP, FP, TN, FN are recorded by manually examining these jsons manually. I.e., comparing annotator tags vs. extraction pattern outcomes, by extract.
