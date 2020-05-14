# place patterns in order of decreasing complexity, such that the most complex if picked up first
extraction_patterns = [
    # complex
    #
    # ----------------
    # <smelly_adj>
    # ----------------
    # stopped around 70-ish
    # collect object referenced as a smell
    #
    # "[<noun>] <verb> <adj>* <smelly_adj> <noun>",
    # with [myrrh] distilled in distant, odorous [indian nights]
    #
    # "<smelly_adj> <noun> _of_ [<noun>]",
    # maloderous flounces of the [apothecary]
    # an aromatic suggesion of the [forest]
    #
    # "<noun> _was_ <smelly_adj> _with_ [<noun>]",
    # the air was pungent with [pine-smoke]
    #
    # ----------------
    # <smelled_verb>
    # ----------------
    # "<smelled_verb> _of|like_ [<noun>] {_and|,|or_ _of_* [<noun>]}*",
    # ...bundle of tiny humanity that smelled of [talcum powder] and of [sachet]
    #
    # "[<noun>] <smelled_verb> <noun>",
    # [the little white and pink flowers] scented the breeze
    #
    # "<smelled_verb> <pronoun> _with_ [<noun>]",
    # "<smelled_verb> <noun> _with_ [<noun>]",
    # she perfumed me with [onions]
    #
    #
    "<noun> smelt_VERB [<noun>]",  #0
    "<pronoun> smelt_VERB [<noun>]",  #0
    # but the dog smelt doggy
    #
    "<noun> <smelt_VERB> _of_ [<noun>]",  #0
    "<pronoun> <smelt_VERB> _of_ [<noun>]",  #0
    # The stranger's room smelt of nothing
    #
    # ----------------
    # <smell_verb>
    # ----------------
    # ------------------
    # <smells_verb>
    # ------------------
    #
    #
    #
    # ------------------
    # <smelling_verb>
    # ------------------
    # ------------------
    # <smell_noun>
    # ------------------
    "<smell_noun> _of_ [<noun>]",  #0
    # smell of fresh, moist paper and newsprint
    #
    "<smell_noun> _of_ [<noun>] _like_ [<noun>]",  #0
    # smell of incense, like the fumes of gunga 103 LAST
    #
    # "[<noun>] <verb> <smell_noun>"
    # [the half open buds upon the trees] shed sweet perfume

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
    #
    #
]
