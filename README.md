----
1_PG_Catalogue (output catalogue.json)/
----
_index the PG catalogue wrt. english language only books_

    $ python3 catalogue.py GUTINDEX.ALL

Returns:
    catalogue.json: a dictionary, by author of all Eng lang books

----
2a_Smellword_frequency (output found,failed.json)/
----
_iden texts with higher frequency of smell words, indicative of higher textual smell experience frequency overall (assumed)_

    $ python3 search_word_frequency.py catalogue.json search_words.txt

Args:
    search_words.txt: text file of smell-associated seed words

Returns:
    found.json: a dictionary of books by total search_word frequency

Notes: PG text is lowercased when matching against search words

----
2b_Analyse_smellword_frequencies/
----
_various plots from 2a data_

yet to be finalised


----
2c_Assemble_datasets/
----
_in order of descending frequency of smell vocab, select 'literature' sources_

found.csv = harvesting/ validation set 
separated into harvesting.csv and validation.csv

----
3_Compare_toolkits/
----

see folders flair/, spaCy/, stanza/ -> scripts parse the same book and report code execution time.

flair: 81s
stanza:16s
spaCy: 5s

TBC: formalise a discussion on the relative accuracy of each toolkit based on studies of wrt. labelled datasets.


----
----
5_Attempt_2/
----
----
_first complete loop (minus effective precision of patterns based on validation set)_

Notes:
* used a single book as a harvesting set, for now
* regex (not re) library must be used. otherwise too slow
* solved unicode export to json problem

----
1a_Extract_text_based.../
----
_return extracts which seed words present_

    $ python3 extract_text.py seed_file.txt

Returns: 
    extracts.json: by book url_code, dictionary of extracts

----
2a_Parse-extracts/
----
_returns spaCy parsed extracts_

    $ python3 DP_spacy.py extracts.json

Returns:
    parsed_extracts.json: by book url_code, lowercased extracts 
    
    Note: extracts are standardised by lowercasing, changing \n and \s+ to \s

----
3a_Collect..../
----

collect_by_patterns2.py
----
_compare parsed extracts to patterns in PATTERNS.py_

* collect extracts to matching pattern, output to terminal for view
* output to terminal all extracts not yet matched
* returns lexicon.json; a lexicon of matched smell-related vocabulary (terms subtended with [] in PATTERNS.py, pattern definition)

    $ python3 collect_by_pattern2.py parsed_extracts.json

PATTERNS.py
----
_PATTERNS.py acts as a high-level abstraction of python re/regex patterns_

The are syntax-simplified patterns identified from examining terminal output of collect_by_patterns2.py, wrt. the unmatched extracts.

* defining token patterns (wrt. spaCy dep_text_pos output) e.g., 
        det__  with match any dep=det token
        _with_ will match any token with text=with
        __ADJ will match any adjective

* in PATTERNS.py or cases can be handles, e.g.,
        _smell|fragrance_ matches _smell_ or _fragrance

* single token repetitions can be handled, e.g.,
        __ADJ* __NOUN would match big red car and big car
        * is zero or more and + is one or more

* group repetitions are handled with {}, e.g,
    (_and|,|or_* __NOUN}* will match the town, county and country

*flag elements to be picked up as match object groups using [] (for lexicon assembly)
    e.g., [__NOUN] _smells_VERB _like_ [__NOUN]

* chunks (defined using the same syntax) defined in CHUNKS.py can be referenced, as a way of creating human readable patterns, that underly flexible and complicated patterns. 

* chunks are denoted by <>
e.g. <noun> <smells_VERB> <prep> <noun>

* where e.g., \<noun> is a noun phrase defined by the pattern "det__* poss__* __PART* <adj>* compound__* _-_* __NOUN|PRON|PROPN+ {_and|,|or_* det__* <adj>* compound__* _-_* __NOUN|PRON|PROPN+}*"

CHUNKS.py
----
_used by PATTERNS.py_
note: later chunks ca reference earlier chunks


----
4_New_extracts_based.../
----
find new extracts based on lexicon.json, returning only those extracts which have not previously been identified.

    $ python3 extract_text.py

Args:
    lexicon.json:
    havesting.csv: 
    previous extracts.json

returns:
    extracts.json



