# Pattern Abstraction

    Performs the conversion of high level patterns defined in libraries/CHUNKS.py and PATTERNS.py into lower level python re/regex lib definitions.
    
## High level language
    
The basic building block is the dependency_word_POS tag ...\
\
E.g.,
    
* To match an unspecified dependency (leave out dependency tag)
```
_word_POS  
```

* To match an unspecified dependency and POS tag
```
_word_
```

* To match multiple words
```
_hello|goobye_
```

* Matching zero or more repetitions
```
{_and|or|,_ _this|that_*}*

# will match "this and that", "this or that", "this, this, that and this, or that"

# Note: * after a token matches zero or more of that tokens
# Note: {}* matches zero or more repetitions of the contents of {}
# Note: + in place of *, matches 1 or more
```

* denote a segment to be extracted
```
[__NOUN] 
```

## Examples

1. Capable of capturing, e.g., "the sweet-scented flowers"

"[<adj>] _-_* <smelly_adj> [<noun> {_of_ <noun>}*]"

Notes:
* <ad>, <noun> and <smelly_adj> are pre-defined chunks defined in /libraries/CHUNKS.py
* [<adj>] and [<noun> {_of_ <noun>}*] are being extracted as lexicon pairs

