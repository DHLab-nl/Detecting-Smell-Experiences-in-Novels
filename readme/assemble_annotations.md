# Assemble recogito annotations into a single reference json (annotations.json)

## Navigate to the folder
```
$cd 6_Evaluation/annotations
```

## Required in folder
*  Recogito annotator tagged text in .xml format, in folders... set{i}/annotator/set{i}.xml

## Assemble a json of annotations from Recogito .xml outputs
output: annotations.json, i.e., our gold standard set of extracts with annotations
```
$python get_annotations.py
```
Note: The number of each annotation tag within annotations.json, can be reported with python3 count_tags.py


