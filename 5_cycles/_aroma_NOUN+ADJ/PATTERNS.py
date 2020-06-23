# place patterns in order of decreasing complexity, such that the most complex is picked up first
extraction_patterns = [
    #----
    #other
    #----
    # and inhale the sweet breath of autumn, which was borne upon gentle gales
    # "[<adj>] _breath_ _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1  FAILED VALIDATION (precision = 0)
    #
    # the soft warm breeze washes in dark fruit, dark flowers...
    "[<adj>] _breeze_ _washes_ _in_ <pronoun>* [<noun> {_of_ <noun>}*]", # 1
    #
    #leaving a faint exhalation of scent and pwoer and delicate perfumes
    # "[<adj>] _exhalation_ _of_ [<noun> {_of_ <noun>}*]",  # 2  #FAILED VALIDATION (prec = 0, n = 1)
    #
    # the air was leaden with (the smell of) <noun>
    "[<adj>] <noun> _was_ _leaden_ _with_ {__DET* <smell_noun> _of_}+ <pronoun>* [<noun> {_of_ <noun>}*]", # 2
    #
    # the mild air, sweet with fading leaves and bracken
    "<noun> {_of_ <noun>}* _,_ [_sweet_] _with_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 3


    #----
    #smell_verb
    #----
    # The very gravel paths and garden mould smell fresh
    "[<noun> {_of_ <noun>}*] <smell_verb> [<adj>*]",  # 2
    #

    # ------------------
    # <smelling_verb>
    # ------------------
    #
    #smelling <adj> wood-smoke
    "<smelling_verb> <pronoun>* [<adj>] [<noun> {_of_ <noun>}*]",  # 2
    #
    #-----------------
    #<smelly_adj>
    #-----------------
    # the sweet-scented flowers
    "[<adj>] _-_* <smelly_adj> [<noun> {_of_ <noun>}*]",  # 1
    #
    # the air was pungent with pine-smoke
    "<noun> _was_ [<adj>* <smelly_adj> <adj>*] _with_ <pronoun>* [<noun> {_of_ <noun>}*]", # 1
    #
    "<noun> _were|was_ [_sweet_ADJ] _with_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    # the air, fragrant with incense smoke
    # "[<adj>* <smelly_adj> <adj>*] _with_* <pronoun>* [<noun> {_of_ <noun>}*]",  # 1 FAILED VALIDATION (p=0.55)
    #
    # with sweet scented, many coloured blossoms, that gave promise of delicios fruit
    "[<adj>] <smelly_adj> _,_* <pronoun>* <noun> _that_ _gave_ __DET* _promise_ _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    # The pungent stifling smoke of powder
    "[<adj>* <smelly_adj> <adj>*] <noun> _of_ [<noun> {_of_ <noun>}*]",  # 1
    #
    # some perfumes are as fragrant of a child
    "_as_ <smelly_adj> _as_ <noun> {_of_ <noun>}*",  # 2
    #
    #
    #----
    #<smells_noun>
    #----
    # the markishley sweet scents of the grass and flowers
    "[<adj>] <smells_noun> _,_* _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    # smells as strong of brandy
    "<smells_noun> _as_ [<adj>] _of_ [<noun> {_of_ <noun>}*]",  # 1
    #
    # ------------------
    # <smell_noun>
    # ------------------
    #
    # the warm aroma of multitudinous exotics
    "[<adj>] <smell_noun> _,_* _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    #what a truly a truly celestial aroma was given off by the fragrant pots of tea
    #
    "[<adj>] <smell_noun> _was_ _given_ _off_ _by_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    # the cool, heavy aroma which one associates with the night
    "[<adj>] <smell_noun> _which_ _one_ _associates_ _with_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    # that [<adj>] aroma in which there is a foretaste of wine
    "[<adj>] <smell_noun> _in_ _which_ _there_ _is_ [<noun> {_of_ <noun>}*]",  # 0
    #
    # the <adj> smell from his great rubber coat
    "[<adj>] <smell_noun> _from_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0  
    #
    #the fragrance breathed from the roses, gardenias
    "[<adj>] <smell_noun> <verb> _from_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    # Amidst the heavy exhilations of these, a Parmesan set a spicy aroma.
    "[<noun> {_of_ <noun>}*] _set_ _a_ [<adj>] <smell_noun>",  # 0
    #
    # the male aroma of him, a mixture of cigar smoke, bay rum and freshly washed hands
    "[<adj>] <smell_noun> _of_ <pronoun> _,_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    "[<adj>] <smell_noun> _of_ <pronoun>* <noun> _,_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    # whose aroma seemed a panting breath
    "[<adj>] <smell_noun> _seemed_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    # that aroma that suggested [a Sunday-school Christmas festival]
    "[<adj>] <smell_noun> _that_ _suggested_ [<noun> {_of_ <noun>}*]", # 0
    #
    # the whitish eye-lashes, forceful freckles, and pungest aroma usually allied to [reddish hair]
    "[<adj>] <smell_noun> _usually_ _allied_ _to_ <pronoun>* [<noun> {_of_ <noun>}*]", # 0
    #
    # perfumed with a [delightful forest] aroma
    "[<adj>] [compound__] <smell_noun>",  # 0
    #
    # the rich aroma distilled from [the creamy hearts of Roman hyacinths]
    "[<adj>] <smell_noun> <verb>* _from_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    #
    "[<adj>] _breeze_ _washes_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    #and inhale the sweet breath of autumn, which was borne upon gentle gales
    "[<adj>] _breath_ _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    # sweet as rose's breath
    "[<adj>] _as_ <pronoun>* [<noun> {_of_ <noun>}*] _breath_", # 1
    #
    # the strong sunlight was an odour in his nostrils
    "[<adj>] [<noun>] _was_ <smell_noun>",  # 1
    #
    # He audaciously draws me by the hair to quaff the sweet wine of his breath, inhaled by him when he watered his favourite bakul-flowers.
    "[<adj>] _wine_ _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    #a most delicious scent, which he found came from the the smell blossoms of the trees. 
    "[<adj>] <smell_noun> _,_* _which_ _he_* _found_* _came_ _from_ <pronoun>* [<noun> {_of_ <noun>}*]", # 1
    #
    #There is a strange unwholesome smell upon the room, like mildewed corduroys....
    "[<adj>] <smell_noun> {_upon_ _the_ <noun>}* _,_* _like_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 1
    #
    #the sweet violets lent fragrance
    "[<adj>] [<noun>] _lent_ <smell_noun>",  # 1
    #
    # the green leaves exhaled a sweet and refreshing fragrance
    "[<noun> {_of_ <noun>}*] _exhaled_ [<adj>] <smell_noun>",  # 1
    #
    # smells as strong of brandy
    "<smell_noun> _as_ [<adj>] _of_ [<noun> {_of_ <noun>}*]",  # 1
    #
    # A subtle fragrance like that of sun-dried seaweed
    "[<adj>] <smell_noun> _like_ {_that_ _of_}* [<noun> {_of_ <noun>}*]",  # 1
    #
    # the <noun> gave out a strong scent
    "[<noun> {_of_ <noun>}*] _gave_ _out_ __DET* [<adj>] <smell_noun>",  # 1
    #
    # the half open buds upon the trees shed there sweet perfume
    "[<noun> {_of|upon_ <noun> }+] _shed_ <pronoun>* [<adj>] <smell_noun>",  # 2
    #
    #faint smell of putrifying bones
    "[<adj>] <smell_noun> _of_ __DET* <pronoun>* <verb> [<noun> {_of_ <noun>}*]",  # 2
    #
    # a yielding surface of leaf-mould, which sent up a warm smell
    "[<noun> {_of_ <noun>}*] _,_* __DET* _sent_ _up_ [<adj>] <smell_noun>",  # 2
    #
    # heavy with the smell of freshly turned soil
    "[<adj>] _with_ __DET* <pronoun>* <smell_noun> _of_ <pronoun>* [<verb> <noun> {_of_ <noun>}*]",  # 2
    #
    # A perfume [heavy] as [incense], sweet as sandlewood
    "<smell_noun> [<adj>] _as_ [<noun> {_of_ <noun>}*]",  # 3
    "<smell_noun> <adj> _as_ <noun> {_of_ <noun>}* _and|,|or_* [<adj>] _as_ [<noun> {_of_ <noun>}*]",  # 3
    #
    # the air was filled with the sweet odor of balsam, spruce and cedar
    "<noun> {_of_ <noun>}* _was_ _filled_ _with_ __DET* [<adj>] <smell_noun> _of_ [<noun> {_of_ <noun>}*]",  # 3

    # ----
    # <smelled_verb>
    # ----
    #
    # the air was perfumed by fallen leaves
    "_was_ <smell_verb> _by_ <pronoun>* [<adj>] [<noun> {_of_ <noun>}*]",  # 1
    #
    # they had perfumed her with scents and essences
    "_had_ <smelled_verb> <pronoun> _with_ [<adj>] [<noun> {_of_ <noun>}*]",  # 1
    #
    # ------------------
    # <smells_verb>
    # ------------------
    #
    # the town smells heartliy of cattle, sheep and malt
    "<smells_verb> <adv>* [<adv>] _of_ [<noun> {_of_ <noun>}*]",  # 2
    #
    #sweet resinous odours from the burning logs
    "[<adj>] <smells_noun> _from_ __DET* <pronoun>* [<verb>* <noun> {_of_ <noun>}*]",  # 3

    ]

identification_patterns = [
    #----
    #other
    #----
    # and inhale the sweet breath of autumn, which was borne upon gentle gales
    "<adj>* _breath_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # the soft warm breeze washes in dark fruit, dark flowers...
    "<adj>* _breeze_ _washes_ _in_ <pronoun>* <noun> {_of_ <noun>}*", # 1
    #
    #leaving a faint exhalation of scent and pwoer and delicate perfumes
    "<adj>* _exhalation_ _of_ <noun> {_of_ <noun>}*",  # 2
    #
    # the air was leaden with (the smell of) <noun>
    "<adj>* <noun> _was_ _leaden_ _with_ {__DET* <smell_noun> _of_}+ <pronoun>* <noun> {_of_ <noun>}*", # 2
    #
    # the mild air, sweet with fading leaves and bracken
    "<noun> {_of_ <noun>}* _,_ _sweet_ _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 3
    #

    #----
    #<smell_verb>
    #----
    "<smell_verb> _that_ <adj>* <noun> {_of_ <noun>}*",  # 1

    # to smell the honeyed air
    "<smell_verb> <noun>",  # 2
    #
    # The very gravel paths and garden mould smell fresh
    "<noun> {_of_ <noun>}* <smell_verb> <adj>",  # 2

    #----
    # <smelling_VERB>
    #
    # the sweet-smelling quince
    "<adv> _-_* <smelling_verb> <noun>",  # 1
    #
    # smelling of the clay
    "<adv>* <smelling_verb> <adv>* _of_ <noun>",  # 2
    #
    #smelling <ad> wood-smoke
    "<smelling_verb> <pronoun>* <adj>* <noun>",  # 2

    # ----
    # <smelly_adj>
    # ----
    # the sweet-scented flowers
    # the pungent smoke
    "<adj>* _-_* <smelly_adj> <noun> {_of_ <noun>}*",  # 1
    #
    # the air was pungent with pine-smoke
    "<noun> _was_ <smelly_adj> _with_ <pronoun>* <noun> {_of_ <noun>}*", # 1
    #
    "<noun> _were_ _sweet_ _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # the air, fragrant with incense smoke
    "<noun> _,_* <smelly_adj> _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 1 
    #
    # with sweet scented, many coloured blossoms, that gave promise of delicios fruit
    "<adj>* <smelly_adj> _,_* <pronoun>* <noun> _that_ _gave_ __DET* _promise_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # The pungent stifling smoke of powder
    "<adj>* <smelly_adj> <adj>* <noun> _of_ <noun> {_of_ <noun>}*",  # 1
    #
    # nearby rosemary-scented hills
    "<noun> _-_ <smelly_adj> <noun> {_of_ <noun>}*",  # 2
    #
    #----
    # <smells_noun>
    #----
    # the markishley sweet scents of the grass and flowers
    "<adj>* <smells_noun> _,_* _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # smells as strong of brandy
    "<smells_noun> _as_ <adj> _of_ <noun> {_of_ <noun>}*",  # 1
    #
    # The air was exquisitely fragrant with earth and flower smells
    "<smells_verb> _with_ <noun> <smells_noun>",  # 2
    

    #----
    # <smell_noun>
    #----

    # "<adj> <smell_noun>",  # 0
    #
    # perfumed with a [delightful forest] aroma
    # "compound__ _-_* <smell_noun>",  # 0
    #
    # Never had an aroma been so sweet, so pervasive
    # "<smell_noun> _been_* _so_ <adj>",  # 0
    #
    # the warm aroma of multitudinous exotics
    "<adj>* <smell_noun> _,_* _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    #what a truly a truly celestial aroma was given off by the fragrant pots of tea
    "<adj>* <smell_noun> _was_ _given_ _off_ _by_ <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    # the cool, heavy aroma which one associates with the night
    "<adj>* <smell_noun> _which_ _one_ _associates_ _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    # that [<adj>] aroma in which there is a foretaste of wine
    "<adj>* <smell_noun> _in_ _which_ _there_ _is_ <noun> {_of_ <noun>}*",  # 0
    #
    # the <adj> smell from his great rubber coat
    "<adj>* <smell_noun> _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 0  
    #
    #the fragrance breathed from the roses, gardenias
    "<adj>* <smell_noun> <verb> _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    # Amidst the heavy exhilations of these, a Parmesan set a spicy aroma.
    "<noun> {_of_ <noun>}* _set_ _a_ <adj>* <smell_noun>",  # 0
    #
    # the male aroma of him, a mixture of cigar smoke, bay rum and freshly washed hands
    "<adj>* <smell_noun> _of_ <pronoun> _,_ <noun> {_of_ <noun>}*",  # 0
    "<adj>* <smell_noun> _of_ <pronoun>* <noun> _,_ <noun> {_of_ <noun>}*",  # 0
    #
    # whose aroma seemed a panting breath
    "<adj>* <smell_noun> _seemed_ <noun> {_of_ <noun>}*",  # 0
    #
    # that aroma that suggested [a Sunday-school Christmas festival]
    "<adj>* <smell_noun> _that_ _suggested_ <pronoun>* <noun> {_of_ <noun>}*", # 0
    #
    # the whitish eye-lashes, forceful freckles, and pungest aroma usually allied to [reddish hair]
    "<adj>* <smell_noun> _usually_ _allied_ _to_ <pronoun>* <noun> {_of_ <noun>}*", # 0
    #
    # perfumed with a [delightful forest] aroma
    "<adj>* compound__ <smell_noun>",  # 0
    #
    # the rich aroma distilled from [the creamy hearts of Roman hyacinths]
    "<adj>* <smell_noun> <verb>* _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    "<adj>* _breeze_ _washes_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    #and inhale the sweet breath of autumn, which was borne upon gentle gales
    "<adj>* _breath_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # sweet as rose's breath
    "<adj>* _as_ <pronoun>* <noun> {_of_ <noun>}* _breath_",  # 1
    #
    # the strong sunlight was an odour in his nostrils
    "<adj>* <noun> _was_ <smell_noun>",  # 1
    #
    # He audaciously draws me by the hair to quaff the sweet wine of his breath, inhaled by him when he watered his favourite bakul-flowers.
    "<adj>* _wine_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    #a most delicious scent, which he found came from the the smell blossoms of the trees. 
    "<adj>* <smell_noun> _,_* _which_ _he_* _found_* _came_ _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    #There is a strange unwholesome smell upon the room, like mildewed corduroys....
    "<adj>* <smell_noun> {_upon_ _the_ _room_}* _,_* _like_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    #the sweet violets lent fragrance
    "<adj>* <noun> _lent_ <smell_noun>",  # 1
    #
    # the green leaves exhaled a sweet and refreshing fragrance
    "<noun> _exhaled_ <adj> <smell_noun>",  # 1
    #
    # smells as strong of brandy
    "<smell_noun> _as_ <adj> _of_ <noun>",  # 1
    #
    # A subtle fragrance like that of sun-dried seaweed
    "<adj>* <smell_noun> _like_ {_that_ _of_}* <noun> {_of_ <noun>}*",  # 1
    #
    # the <noun> gave out a strong scent
    "<noun> {_of_ <noun>}* _gave_ _out_ __DET* <adj>* <smell_noun>",  # 1
    #
    # the half open buds upon the trees shed there sweet perfume
    "<noun> {_of|upon_ <noun> }+ _shed_ <pronoun>* <adj>* <smell_noun>",  # 2
    #
    #faint smell of putrifying bones
    #faint sweet smell of burning cedar
    "<adj>* <smell_noun> _of_ __DET* <pronoun>* <verb> <noun> {_of_ <noun>}*",  # 2
    #
    # a yielding surface of leaf-mould, which sent up a warm smell
    "<noun> {_of_ <noun>}* _,_* __DET* _sent_ _up_ <adj>* <smell_noun>",  # 2
    #
    # heavy with the smell of freshly turned soil
    "<adj> _with_ __DET* <pronoun>* <smell_noun> _of_ <pronoun>* <verb> <noun> {_of_ <noun>}*",  # 2
    #
    # A perfume [heavy] as [incense], sweet as sandlewood
    "<smell_noun> <adj> _as_ <noun> {_of_ <noun>}*",  # 3
    "<smell_noun> <adj> _as_ <noun> {_of_ <noun>}* _and|,|or_* <adj>* _as_ <noun> {_of_ <noun>}*",  # 3
    #
    # the air was filled with the sweet odor of balsam, spruce and cedar
    "<noun> {_of_ <noun>}* _was_ _filled_ _with_ __DET* <adj>* <smell_noun> _of_ <noun> {_of_ <noun>}*",  # 3
    #
    # ----
    # <smelled_verb>
    # ----
    #
    # the air was perfumed by fallen leaves
    "_was_ <smell_verb> _by_ <pronoun>* <adj>* <noun> {_of_ <noun>}*",  # 1
    #
    # they had perfumed her with scents and essences
    "_had_ <smelled_verb> <pronoun> _with_ <noun> {_of_ <noun>}*",  # 1
    #
    # he had never seen or smelled such exquisite flowers
    "<smelled_verb> _such_* <adj>* <noun> {_of_ <noun>}*",  # 1
    #
    # smelled of some curious sickish-sweet perfume
    "<smelled_verb> <adv>* _of_ __DET* <adj>* <pronoun>* <noun>",  # 2
    #
    # the mounains perfumed with flowers from a valley of roses
    "<smelled_verb> <adv>* _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 2
    #
    # ------------------
    # <smells_verb>
    # ------------------
    # the tea smells delicisously
    # "<noun> {_of_ <noun>}* <smells_verb> <adv>",  #2 BASIC
    #
    # the town smells heartliy of cattle, sheep and malt
    "<smells_verb> <adv>* _of_ <noun> {_of_ <noun>}*",  # 2
    #

    "<adj>* <smells_noun> _from_ __DET* <pronoun>* <verb>* <noun> {_of_ <noun>}*",  # 3
]
