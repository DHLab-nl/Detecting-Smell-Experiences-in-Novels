# Calculate inter-annotator agreement wrt. set0

## Navigate to the folder
```
$cd 6_Evaluation/annotations
```

Note: command line ouput of each annotator pairs cohen kappa score
```
$python3 agreement.py set0 "['d', 'o']"  # where either 'd' or 'o' considered a match
$python3 agreement.py set0 "['o']"  # where tag 'o' only matches 
$python3 agreement.py set0 "['v']"  # where tag 'v' only matches 
```
