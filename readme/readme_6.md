# Evaluation of the methodology outcomes

## Assemble gold standard into a single reference json

### Navigate to the folder
```
$cd 6_Evaluation/annotations
```

### Required in folder
*  Recogito annotator tagged text in .xml format, in folders... set{i}/annotator/set{i}.xml

### Assemble a json of annotations from Recogito .xml outputs
output: annotations.json
```
$python get_annotations.py
```

### calculate inter-annotator agreement wrt. set0

Note: command line ouput of each annotator pairs cohen kappa score
```
$python3 agreement.py set0 "['d', 'o']"  # where either 'd' or 'o' considered a match
$python3 agreement.py set0 "['o']"  # where tag 'o' only matches 
$python3 agreement.py set0 "['v']"  # where tag 'v' only matches 
```

## Evaluate the identification_patterns against the gold standard

### Navigate to the folder
```
$cd 6_Evaluation/gold_standard
```

### Required in folder
* annotations.json\
symbolic link to 6_Evaluation/annotations/annotations.json
* folder _aroma_NOUN+VERB, containing PATTERNS.py from the iterative bootstrapping runs
* folder _aroma_NOUN+ADJ, containing PATTERNS.py from the iterative bootstrapping runs
* folder reference_scenario, containing PATTERNS.py with a list of high smell association keywords
* libraries : a symbolic link to 5_Process/libraries

### flag each pattern of identification_patterns matching or failure to match against the gold standard as TP, FP, TN, FN

Where n is the number of parallel processes to run (e.g., 4)
```
$python3 outcomes_by_pattern.py n _aroma_NOUN+ADJ
$python3 outcomes_by_pattern.py n _aroma_NOUN+VERB
$python3 outcomes_by_pattern.py n reference_scenario
```

###Output
*outcomes__aroma_NOUN+ADJ.json
*outcomes__aroma_NOUN+VERB.json
*outcomes_reference_scenario.json

## Calculate the precision & recall of each identification pattern wrt. the gold standard AND calculate the groups prediction precision and recall wrt. a specified minimum precision threshold, above which a pattern is included in group prediciton

*One or more identification patterns in a group prediction, matching against a sentence, is a group prediction of positive*

Note: in outocomes__folder.json, we have a list of TP, FP, TN, FN records by pattern.
Thus,
* gold standard = True, 
```

```










