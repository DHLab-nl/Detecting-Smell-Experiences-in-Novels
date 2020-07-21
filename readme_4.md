# Create the Gold Standard

Assemble x documents, of y random extracts from test.json. A proportion of the extracts, z, contain at least one high smell association keyword.

## Requires in folder:
* test.json
A symbolic link to /3_Create_Datasets/datasets/test.json

* search_words.txt
a list high smell association keywords

```
$cd 4_Gold_Standard
$python3 assemble_test.py x y z
```

## Output
/samples/test_set-{i}.txt, for i = 1..x



