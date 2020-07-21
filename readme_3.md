# Creating Harvesting, Validation and Evaluation datasets
    
    Create spaCy parsed harvesting, validation and evaluation datasets
    Each sentence in each dataset is passed to spaCy, each token tagged as dependency_word_POS for pattern matching

# Requires in folder:
* harvesting.csv, test.csv and validation.csv are assembled from found.csv, removing repetitions, and non target texts
    
# Run...
```
# where n is the number of parallel threads to run...
$cd 3_Create_Datasets
$python3 get_dataset_multiprocessor.py harvesting.csv n
$python3 get_dataset_multiprocessor.py harvesting.csv n
$python3 get_dataset_multiprocessor.py harvesting.csv n
```
# Output
./dataset/harvesting.json
./dataset/validation.json
./dataset/testing.json

E.g., each book of a collection is broken down into sentences via NLTK.tokenize, lowercased, and parsed by spaCy.

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




