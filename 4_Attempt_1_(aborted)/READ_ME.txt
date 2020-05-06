
Identified Patterns:
---------------------
KEY:
    * zero or more
    + 1 or more
    each token is listed in terms of (dep, text, pos), where dep, pos are spaCy tags
    {} groups on tokens
    <> tokens to retrieve in a smell language lexicon
    e.g. *('det',,'DET') means zero or more dets
         *{(,'and',) (,,NOUN)} zero or more groups of consecutive ADJ NOUNS


OBSERVED PATTERNS: 
-----
('ROOT', 'scent', 'VERB') ('dobj',,'PRON') ('prep', 'with', 'ADP') ('amod',, 'ADJ') <<(,, 'NOUN')>>
-----
returns NOUNS
-----
e.g.
('nsubj', 'I', 'PRON'), ('aux', 'will', 'VERB'), ('ROOT', 'scent', 'VERB'), ('dobj', "'em", 'PRON'), ('prep', 'with', 'ADP'), ('amod', 'best', 'ADJ'), ('pobj', 'vanilla', 'NOUN')


-----
('nsubj',, 'PRON'), ('ROOT', 'smells', 'VERB'), <<(,,'ADJ')>>
-----
returns ADJ
-----
e.g.
('nsubj', 'It', 'PRON'), ('ROOT', 'smells', 'VERB'), (, 'comforting', 'ADJ')


-----
('det'),,'DET') <<*('compound',, 'NOUN') (,, 'NOUN')>> ('ROOT',, 'VERB') ('aux', 'to', 'PART') ('xcomp', 'smell', 'VERB')
-----
return NOUNS
-----
e.g.
('det, 'the', 'DET') ('compound', 'kerosene', 'PROPN'), ('nsubj', 'lamps', 'PROPN'), ('ROOT', 'began', 'VERB'), ('aux', 'to', 'PART'), ('xcomp', 'smell', 'VERB')


-----
('nsubj',,) *('aux','VERB') *('advmod',,'ADV') ('ROOT', 'smell', 'VERB') *('det',,'DET') <<*{(,,'PROPN') (,,'PART')} ('amod',,'ADJ') *('compound','NOUN') *('punct','-', 'PUNCT') ('dobj',,'NOUN')>> <<*{(, 'and|,', 'CCONJ') *('det',,'DET') *('amod',, 'ADJ') ('pobj',,'NOUN')
-----
Return Nouns
-----
e.g.


-----
*('det', 'DET') ('amod','fetid|smelly|scented','adj') <<('compound',,'NOUN') ('pobj|dobj',,'noun')>>
-----
Returns NOUN
-----
e.g. 
('det', 'the', 'det'), ('amod', 'fetid', 'adj'), <<('pobj', 'burrow', 'noun')>>

('amod', 'heavy', 'ADJ'), ('punct', ',', 'PUNCT'), ('amod', 'scented', 'ADJ'), <<('pobj', 'flowers', 'NOUN')>>


-----
('det',,'DET') <<('nsubj',, 'NOUN')>> ('conj', 'smelt', 'VERB') <<(,, 'ADJ')>>
-----
Returns (subject, adjective describing smell) pair
-----
e.g.
('det', 'the', 'DET'), ('nsubj', 'sea', 'NOUN'), ('conj', 'smelt', 'VERB'), ('acomp', 'good', 'NOUN')


-----
('det',,'DET') + *(advmod,,'ADV') *('amod',,'VERB') ('amod',,'ADJ') ('pobj|dobj|conj|ROOT|nsubj','reek|stench|smell|scent', 'NOUN') *('ROOT',,'VERB') ('prep', 'of', 'ADP') *('det',,'DET') *('poss',,'NOUN') <<*('amod',,'ADJ') *('compound|pcomp',,'NOUN|PROPN') *(,'-',) ('pobj|'dobj',,'NOUN|PROPN') *{('prep', ,'ADP') *('poss',,'DET') ('pobj',,'NOUN|PRON')}>> +{(,'and|,',) *('amod',,'ADJ') *(,,'VERB') ('conj|dobj',,'NOUN'})
-----
returns NOUNs
-----
('det', 'the', 'DET'), ('dobj', 'scent', 'NOUN'), ('prep', 'of', 'ADP'), ('amod', 'damp', 'ADJ'), ('compound', 'wood', 'NOUN'), ('pobj', 'smoke', 'NOUN'), ('punct', ',', 'PUNCT'), ('amod', 'hot', 'ADJ'), ('conj', 'cakes', 'NOUN'), ('punct', ',', 'PUNCT'), ('acl', 'dripping', 'VERB'), ('dobj', 'undergrowth', 'ADJ'), ('punct', ',', 'PUNCT'), ('cc', 'and', 'CCONJ'), ('conj', 'rotting', 'VERB'), ('compound', 'pine', 'NOUN'), ('punct', '-', 'PUNCT'), ('dobj', 'cones', 'NOUN'), ('punct', '.', 'PUNCT')

('det', 'the', 'DET'), ('advmod', 'well', 'ADV'), ('punct', '-', 'PUNCT'), ('amod', 'remembered', 'VERB'), ('pobj', 'smell', 'NOUN'), ('prep', 'of', 'ADP'), ('det', 'the', 'DET'), ('pobj', 'East', 'PROPN')

('det', 'The', 'DET'), ('nsubj', 'smell', 'NOUN'), ('ROOT', 'reminded', 'VERB'), ('dobj', 'Dick', 'PROPN'), ('prep', 'of', 'ADP'), ('compound', 'Monsieur', 'PROPN'), ('pobj', 'Binat', 'PROPN')


-----
('amod',, 'ADJ'), ('nsubj',, 'NOUN'), ('ROOT', 'smells', 'NOUN')
-----
('amod', 'spicy', 'ADJ'), ('nsubj', 'garlic', 'PROPN'), ('ROOT', 'smells', 'NOUN')
