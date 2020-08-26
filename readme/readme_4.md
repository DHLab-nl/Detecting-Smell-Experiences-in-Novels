# Create the Gold Standard

Assemble x documents, of y random extracts from test.json.\
A proportion of the extracts, z, contain at least one high smell association keyword.

## Navigate to folder
```
$cd 4_Gold_Standard
```

## Requires in folder:
* test.json
A symbolic link to 3_Create_Datasets/datasets/test.json

* search_words.txt
a list high smell association keywords

## Run...
```
$python3 assemble_test.py x y z
```

## Output
/samples/test_set-{i}.txt, for i = 1..x

## Further work
Annotators asked to annotate the spans as per [the annotation guidelines](/6_Evaluation/annotation guidelines/Annotation Guidelines.odt)


