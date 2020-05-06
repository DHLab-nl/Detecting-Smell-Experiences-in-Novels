# place patterns in order of decreasing complexity, such that the most complex if picked up first
patterns = [
    # ----------------
    # <smelly_adj>
    # ----------------
    #
    "<aux>* <adv>* <smelly_adj> [<noun>]",
    # the smelly leather (adj, noun)
    #
    # ----------------
    # <smelled_verb>
    # ----------------
    #
    "[<noun>] <smelled_verb> <prep> [<noun>]",
    # the banana  trees smelled of banana, suprisingly (returns: noun, noun)
    #
    "[<noun>] <smelled_verb> [<adj>]",
    # (the sea) smelt (good) -> (return: noun, adj)
    #
    "<smelled_verb> <prep>* [<noun>*]",
    # he sniffed hungrily
    # he sniffed at the air
    # they smelled [lavender] -> (returns: noun)
    #
    # ----------------
    # <smell_verb>
    # ----------------
    #
    "<smell_verb> [<noun>] _with_ [<noun>]",
    # fragance (the sauce) with (vanilla) -> (returns: noun, noun)
    #
    "[<noun>] <aux>* <smell_verb> <prep>* [<noun>]",
    # i smell the dawn
    # your things smell of tobacco and blood
    # the (wildflowers) smell of (chocolate and bitter coffee) -> (return: noun, noun)
    #
    "<aux> <smell_verb> [<noun>]",
    # could smell the (acrid wood-smoke) (return: noun)
    #
    "[<noun>] <verb> _to_ <adv>* <smell_verb> [<adv>]",
    # (the oranges) are starting to really smell (bad) -> (returns: noun, adj)
    #
    "[<noun>] <aux> <smell_verb> [<adj>]",
    # the gills should also smell sweet -> returns: (noun, adj)
    # does calc
    # ------------------
    # <smells_verb>
    # ------------------
    #
    "[<noun>] <adv>* <smells_verb> [<adv>]",
    # (the apple) smells (bad) -> (returns: noun, adj)
    #
    # ------------------
    # <smell_noun>
    # ------------------
    #
    "[<adj>] <smell_noun> <prep> [<noun>]",
    # horrible stench of stale brick kilns
    # the room was filled with the (most stickening stench) of (roses) -> (returns:adj, noun)
    #
    "[<adj>] <smell_noun> <verb> [<noun>]",
    # the most (sickening) stench pervaded the entire (amphitheatre). (adj, noun)
    #
    "<smell_noun> <prep> [<noun>]",
    # there was a scent of (heliotrope) -> (returns: noun)
    #
    "<verb>* [<noun>] <verb>* <adj> <smell_noun>",
    # have the flowers less fragrance
    # the (flowers) have less (fragrance) -> (Returns: noun, noun)
    #
    "<smell_noun> <verb> [<adj>]",
    # the smell was very (strong) -> (adj)
    #
    "[<noun>] <verb> <smell_noun> [<noun>]",
    #the (rooms) were filled with the scents of (lavender) -> (returns: noun, noun)
    #
    "<smell_noun> _,_* <prep>* [<noun>]",
    # a verb (bad stink), (this place) -> (returns: adj, noun)
    #
    # ------------------
    # <smells_noun>
    # ------------------
    #
    "[<adj>] <smells_noun>",
    # there were several (strong) smells -> (adj)
    #
    "<smell_noun> [<verb>]",
    # the stinks (rose up and overwhelmed us)
]
