# Creating Harvesting, Validation and Evaluation datasets
    
    Create spaCy parsed harvesting, validation and evaluation datasets
    Each sentence in each dataset is passed to spaCy, each token tagged as dependency_word_POS for pattern matching
    
## Navigate to folder
```
$cd 3_Create_Datasets
```

## Requires in folder:
* harvesting.csv, test.csv and validation.csv, MANUALLY assembled from 2_Rank_Catalogue/found.csv, removing repetitions, and non target texts
    
## Run...
where n is the number of parallel threads to run...
```
$python3 get_dataset.py harvesting.csv n
$python3 get_dataset.py validation.csv n
$python3 get_dataset.py test.csv n
```
## Output
datasets/output.json

Example format of outputs' parsed text:

{
    "book_code":[
                    (
                        "the cat sat on the mat", 
                        "det_the_DET nsubj_cat_NOUN ROOT_sat_VERB prep_on_ADP det_the_DET pobj_mat_NOUN"
                    ), 
                    ...
                ], 
                ...
}




