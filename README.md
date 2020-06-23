0_embeddings/
-
_investigate the top 100 tokens (from the Google news dataset) with the highest cosine similarity to 'smell' (output to term)_

    %python3 embeddings.py

1_PG_Catalogue (output catalogue.json)/

-
_index the PG catalogue wrt. english language only books_

    $ python3 catalogue.py GUTINDEX.ALL

Returns:
    catalogue.json: a dictionary, by author of all Eng lang books
    {"author":[('book_title', 'url_code'), ...], ...}

2a_Smellword_frequency (output found.json, found.csv)/10May_multithreaded/
-
_rank texts by smell word frequency (as indicative of overall experience frequency_
(note: written via threading module to avoid i/o bottlenecks)

    $ python3 search_word_frequency.py

Requires in directory:
    catalogue.json
    search_words.txt: text file of smell-associated seed words

Returns:
    found.json: a dictionary of books by total search_word frequency
    {
    "frequency":[
                     ["author", "title", "url_code", ("matched", "words", "list")],
                     ...
                ], 
                ...
    }
    
_reformat found.json to found.csv_

    $ python3 output_to_csv.py
    
Required in directory:
    found.json

Returns:
    found.csv: a csv
    ,freq.,title,author,words

Notes: 
    * PG text is lowercased when matching against search words
    * seed words taken from Cambridge online...conjugate forms included
    * uses the python threading module (10 threads, each of approx 3000 books), results in 5x speed up (5h 18m instead of 24+ hours)

2b_Analyse_smellword_frequencies/
-
_various plots from 2a data_

yet to be finalised


2c_Assemble_datasets/11May 
-
(output:, harvesting_set.json, test_set.json, validation_set.json)
-
_in order of descending frequency of smell vocab, select 'literature' sources_

books evaluated manually as to whether 'literature' or other.
vim macros (added to init.vim) used to speed up the process:

* delete from file and append to non-literature.csv
let @q="1:w >> non-literature.csv\<CR>dd"

* copy the title, author string into clipboard, ready for web search
let @a='f,f,l"+yt"^'

* delete from file and append to repetitions.csv
let @r="1:w >> repetitions.csv\<CR>dd"

found.csv = harvesting/ validation set 
separated into harvesting.csv and validation.csv

**once the lists, harvesting.csv, test.csv and validation.csv are assembled, produce a (spaCy) parsed dataset of each**

Example:
    $ python3 get_dataset_multiprocessor.py list.csv n

Args:
    list.csv: a list of books from which to harvest extracts.
    n: number of parallel processes to start (< number of pc threads)

Outputs:
    dataset.json {book_code: list of sentences}, where sentences are lists of word_POS
    Note: perform for each of harvesting, test and validation set
"""

2d_annotated_set
-
Assemble sets of extracts, taken from test.json, into x sets of y extracts.
z is the ratio of keyword extracts to random extracts.

Example:
    $ python3 assemble_test.py x y z
    $ python3 assemble_test.py 10 100 0.8

Args:
    - x (int): number of sets to assemble
    - y (int): number of extracts per set
    - z (float): proportion of extracts to contain keywords

Requires in directory:
    test.json: {"book_code": [list of sentence, parsed sentence tuples],.. }
"""

3_Compare_toolkits/
-

see folders flair/, spaCy/, stanza/ -> scripts parse the same book and report code execution time.

flair: 81s
stanza:16s
spaCy: 5s

TBC: formalise a discussion on the relative accuracy of each toolkit based on studies of wrt. labelled datasets.


5_cycles
-
Notes:
* regex (not re) library must be used. otherwise too slow
* solved unicode export to json problem

seed lexicon.json with seedword
    e.g. [[[["_aroma_"]]]]

run cycles of .....

A) 
    $python3 get_extracts_multiprocessor 4

i.e., auto retrieve sentences with (previous round) of lexicon.json entries present

B) 
    manually evalute extracts-x.txt for patterns
    add the patterns to PATTERNS.py

C) 
    $python3 update_lexicon_multiprocess.py

i.e., auto retrieve vocabulary matching patterns

D)  
    $python3 modify_lexicon.py

cycle specific modification of lexicon.
e.g., when considering objects as reference smells, amending _text_DET to _text_DET*

