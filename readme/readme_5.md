# Iterative Bootstrapping Process

## Navigate to folder:
```
$cd 5_Process
```

## Requires in folder:
* [libraries/pattern_abstraction.py](readme_pattern_abstraction.md)
* [libraries/CHUNKS.py](readme_chunks.md)

* datasets/harvesting.json\
symbolic link to 3_Create_Datasets/datasets/harvesting.json

* datasets/validation.json\
symbolic link to 3_Create_Datasets/datasets/validation.json

## Run...
E.g., targeting NOUN and ADJ features, seeding with "_aroma_NOUN"

### Create a subfolder to store info, initialise PATTERNS.py, initialise lexicon.json
```
$mkdir _aroma_NOUN+ADJ
$cp libraries/PATTERNS_template.py _aroma_NOUN+ADJ/PATTERNS.py
$touch _aroma_NOUN+ADJ/lexicon.json
$echo "[[[[[\"_aroma_NOUN\"]]]]]" >> _aroma_NOUN+ADJ/lexicon.json
```

### Cyclically do the following:

1. Get (unseen) extracts from the harvesting set, that do not conform to a known (identification) patterns in PATTERNS.py, based on the last round of lexicon entries the extraction_patterns list the extraction_patterns list.
 
* PATTERNS.py contains two lists:
    * **identification patterns**\ i.e., a list of any and all observed patterns, which match the desired textual relationship;\
    E.g., "<adj>* _exhalation_ _of_ <noun> {_of_ <noun>}*"
    * **extraction patterns**\ i.e., lists of the subset of patterns in [high-level format](readme_pattern_abstraction.md), used to populate the lexicon.\
    E.g., "[<adj>] _-_* <smelly_adj> [<noun> {_of_ <noun>}*]"

```
$python3  get_extracts.py 4 _aroma_NOUN+ADJ
# note: the 4 is the number of parallel processes to start (change as preferred)
```

2. Manually examine extracts-{i}.txt, where i is the current cycle, for new patterns. Add observed, new patterns to PATTERNS.py as high level [abstractions](readme_pattern_abstraction.md)
    * Any and all patterns relevant to smell extracts are defined in the list, identification_patterns
    * that subset of identification_patterns that can be used to target the targeted COINCIDENT lexicon features are added to the extraction_patterns list

3. Validate the proposed identification patterns against the validation set:

* get a sample of (10) extracts that conform to each pattern, if present in the validation set
```
$python3 validate.py 4 _aroma_NOUN+ADJ
# where 4 is the number of concurrent threads (change as appropriate)
```

* Annotate the validation_{pattern}.json file extract samples, and mark as TP, FP or U; for true positive, false positive and unknown respectively. U (Unknown) examples are omitted from precision estimates. 
 
* Estimate the precision of the pattern
```
$python3 validation_statistics.py _aroma_VERB+ADJ
```

* Amend PATTERNS.py depending on selection/ threshold criteria for including patterns.i.e., remove patterns below a user-defined validation precision threshold.

4. Update the lexicon, based on the new extraction_patterns in PATTERNS.py
```
$python3 update_lexicon.py 4 _aroma_NOUN+ADJ
# where 4 is the number of concurrent threads (change as appropriate)
```

REPEAT

# Output
PATTERNS.py, specifically the identification patterns
