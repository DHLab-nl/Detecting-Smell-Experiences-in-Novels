# place patterns in order of decreasing complexity, such that the most complex if picked up first
extraction_patterns = [
    # ------------------
    # <smells_verb>
    # ------------------
    "<smells_verb> _of_ <noun>", #0
    #
    # ------------------
    # <smelling_verb>
    # ------------------
    # ------------------
    # <smell_noun>
    # ------------------
    #
    "[<noun>] _-_ <smell_noun>", #0
    # but from the tepee had come the man-smell
    #
    "<smell_noun> _of_ <pronoun>* [<noun>]",  #0
    # smell of fresh, moist paper and newsprint
    # smell of his cassock
    #
    "<smell_noun> _of_ [<noun>] _like_ [<noun>]",  #0
    # smell of incense, like the fumes of gunga 103 LAST
    #
    "<smell_noun> _o_ _'_ [<noun>]", #0 
    #
    # ------------------
    # <smells_noun>
    # ------------------
]

identification_patterns = [
    #----
    #<smelly_adj>
    #----
    # "<smelly_adj> <noun>",
    #
    # "<smelly_adj> was <noun>",
    # "<smelly_adj> was <pronoun>",
    # so pungent was it
    #
    #----
    #<smelled_verb>
    #----

    #----
    #<smell_noun>
    #----
    "<adj> <smell_noun>", #0
    # The fallowed earth gave forth a fresh, pleasant smell.
    #
    "_like_ <smell_noun>", #0
    # Like the smell that spread around Cucugnan, ...
    #
]
