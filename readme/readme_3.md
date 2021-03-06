# Creating Harvesting, Validation and Evaluation datasets
    
    Create spaCy parsed harvesting, validation and evaluation datasets
    Each sentence in each dataset is passed to spaCy, each token tagged as dependency_word_POS for pattern matching
    
## Navigate to folder
```
$cd 3_Create_Datasets
```

## Requires in folder:
* harvesting.csv, test.csv and validation.csv, MANUALLY assembled from 2_Rank_Catalogue/found.csv, removing repetitions, and non-target (i.e., non 'literature') texts
    
## Run...
where n is the number of parallel threads to run...
```
$python3 get_dataset.py harvesting.csv n
$python3 get_dataset.py validation.csv n
$python3 get_dataset.py test.csv n
```
## Args
n (int): number of parallel processes to run

## Returns
datasets/output.json

Example format of outputs' parsed text:

{\
    "book_code":[\
                    (\
                        "the cat sat on the mat", \
                        "det_the_DET nsubj_cat_NOUN ROOT_sat_VERB prep_on_ADP det_the_DET pobj_mat_NOUN"
                    ), \
                    ...\
                ], \
                ...\
}

# Note: Rename the resulting output.json to harvesting.json, test.json or validation.json as appropriate



