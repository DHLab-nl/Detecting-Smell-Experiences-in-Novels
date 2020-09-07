# Determine the prediction outcomes by sentence, by pattern

    i.e., identify individual pattern matches as TP, FP, TN or FN

## Navigate to the folder
```
$cd 6_Evaluation/gold_standard
```

## Required in folder
* annotations.json\
symbolic link to 6_Evaluation/annotations/annotations.json;
* folder _aroma_NOUN+ADJ, containing PATTERNS.py, consisting of identification patterns, from the iterative bootstrapping runs;
* folder _aroma_NOUN+VERB, containing PATTERNS.py, consisting of identification patterns, from the iterative bootstrapping runs;
* folder reference_scenario, containing PATTERNS.py, consisting of identification patterns based on keywords only, from the iterative bootstrapping runs;
* folder implementation1+implementation2 containing PATTERNS.py, consisting of identification patterns from both implementations, from the iterative bootstrapping runs;
* libraries : a symbolic link to 5_Process/libraries

## Run
Where n is the number of parallel processes to run (e.g., 4)
```
$python3 outcomes_by_pattern.py n _aroma_NOUN+ADJ
$python3 outcomes_by_pattern.py n _aroma_NOUN+VERB
$python3 outcomes_by_pattern.py n reference_scenario
```

##Output
*./prediction_labels_patterns/prediction_labels__aroma_NOUN+ADJ.json
*./prediction_labels_patterns/prediction_labels__aroma_NOUN+VERB.json
*./prediction_labels_patterns/prediction_labels__aroma_implementation1+implementation2.json
*./prediction_labels_patterns/prediction_labels__aroma_reference_scenario.json

