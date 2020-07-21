# Iterative Bootstrapping Process

## Requires in folder:
* [libraries/pattern_abstraction.py](readme/readme_pattern_abstraction.md)
* [libraries/CHUNKS.py](readme/readme_chunks.md)

* datasets/harvesting.json
symbolic link of 3_Create_Datasets/datasets/harvesting.json

* datasets/validation.json
symbolic link of 3_Create_Datasets/datasets/validation.json

## Run...
E.g., targeting NOUN and ADJ features, seeding with _aroma_NOUN

### Create a subfolder to store info, initialise PATTERNS.py, initialise lexicon.json
```
$cd 5_Process
$mkdir _aroma_NOUN+ADJ
$cp libraries/PATTERNS_template.py _aroma_NOUN+ADJ/PATTERNS.py
$touch _aroma_NOUN+ADJ/lexicon.json
$echo "[[[[[\"_aroma_NOUN\"]]]]]" >> _aroma_NOUN+ADJ/lexicon.json
```

### Cyclically do the following:

1. get (unseen) extracts from the harvesting set (that do not conform to a known pattern in Patterns), based on the last round of lexicon entriesthe extraction_patterns list the extraction_patterns list
```
$python3  get_extracts.py 4 _aroma_NOUN+ADJ
# note: the 4 is the number of parallel processes to start (change as preferred)
```


2. Manually examine extracts-{i}.json, where i is the current cycle, for new patterns. Add new patterns to PATTERNS.py as high level abstractions:
    * Any and all patterns relevant to smell extracts are defined in the list, identification_patterns
    * that subset of identification_patterns that can be used to target the targeted lexicon features are added to the extraction_patterns list


3. Validate the proposed identification patterns against the validation set:

* get a sample of (10) extracts that conform to each pattern, if present in the validation set
```
$python3 validate.py 4 _aroma_VERB+ADJ
# where 4 is the number of concurrent threads (change as appropriate)
```

* Annotate the validation_{pattern}.json file extract samples, and mark as TP, FP or U (unknown)
 
* Estimate the precision of the pattern
```
$python3 validation_statistics.py _aroma_VERB+ADJ
```

* Amend PATTERNS.py depending on selection/ threshold criteria for including patterns.

4. Update the lexicon, based on the new extraction_patterns in PATTERNS.py
```
$python3 update_lexicon.py 4 _aroma_VERB+ADJ
# where 4 is the number of concurrent threads (change as appropriate)
```

REPEAT

# Output
PATTERNS.py, specifically the identification patterns
