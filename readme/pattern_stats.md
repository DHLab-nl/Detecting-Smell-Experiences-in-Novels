# Produce individual pattern / group pattern recall and precision statistics

##Navigate to
```
cd 6_Evaluation/gold_standard
```

##Requires in folder
* The output from prediction_labels_by_pattern.py

## Run
```
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.99
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.95
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.90
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.85
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.80
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.75
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.70
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.60
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.50
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.40
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.30
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.20
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0.10
$python3 precision_recall_stats.py _aroma_NOUN+ADJ 0

$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.99
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.95
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.90
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.85
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.80
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.75
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.70
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.60
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.50
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.40
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.30
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.20
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0.10
$python3 precision_recall_stats.py _aroma_NOUN+VERB 0

$python3 precision_recall_stats.py implementation1+implementation2 0.99
$python3 precision_recall_stats.py implementation1+implementation2 0.95
$python3 precision_recall_stats.py implementation1+implementation2 0.90
$python3 precision_recall_stats.py implementation1+implementation2 0.85
$python3 precision_recall_stats.py implementation1+implementation2 0.80
$python3 precision_recall_stats.py implementation1+implementation2 0.75
$python3 precision_recall_stats.py implementation1+implementation2 0.70
$python3 precision_recall_stats.py implementation1+implementation2 0.60
$python3 precision_recall_stats.py implementation1+implementation2 0.50
$python3 precision_recall_stats.py implementation1+implementation2 0.40
$python3 precision_recall_stats.py implementation1+implementation2 0.30
$python3 precision_recall_stats.py implementation1+implementation2 0.20
$python3 precision_recall_stats.py implementation1+implementation2 0.10
$python3 precision_recall_stats.py implementation1+implementation2 0

$python3 precision_recall_stats.py reference_scenario 0.99
$python3 precision_recall_stats.py reference_scenario 0.95
$python3 precision_recall_stats.py reference_scenario 0.90
$python3 precision_recall_stats.py reference_scenario 0.85
$python3 precision_recall_stats.py reference_scenario 0.80
$python3 precision_recall_stats.py reference_scenario 0.75
$python3 precision_recall_stats.py reference_scenario 0.70
$python3 precision_recall_stats.py reference_scenario 0.60
$python3 precision_recall_stats.py reference_scenario 0.50
$python3 precision_recall_stats.py reference_scenario 0.40
$python3 precision_recall_stats.py reference_scenario 0.30
$python3 precision_recall_stats.py reference_scenario 0.20
$python3 precision_recall_stats.py reference_scenario 0.10
$python3 precision_recall_stats.py reference_scenario 0

```

##output
* Individual pattern precision and recall stats. See /precion_recall_stats_patterns.
* Group prediction outcomes, pattern groups including those patterns with an individual precision about the specific cutoff level. See prediction_labels_group/;
