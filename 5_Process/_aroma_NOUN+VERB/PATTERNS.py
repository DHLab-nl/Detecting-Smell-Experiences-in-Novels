extraction_patterns = [
    # -----
    # other
    # -----
    # the heavy fumes of incense rose up
    "_fumes_ _of_ [_incense_ {_of_ <noun>}*] __DET* [<verb> prep__*]",  # 1
    # ----
    # <smell_verb>
    # ----
    # i smell the fog that hung about the place
    "<smell_verb> [<noun> {_of_ <noun>}*] __DET* [<verb> prep__*]",  # 1
    #
    #
    # ------------------
    # <smells_verb>
    # ------------------
    #
    # ------------------
    # <smelling_verb>
    # ------------------
    #     # reeking with smoke and fog
    "[<smelling_verb> _with_] [<noun> {_of_ <noun>}*]",  # 2
    #
    # next came the strong smelling cheeses
    "[<verb> prep__*] __DET* <pronoun>* <adj>* <smelling_verb> [<noun> {_of_ <noun>}*]",  # 1 
    #
    # ------------------
    # <smell_noun>
    # ------------------
    #
    # the smell of burning tobbaco came from
    "<adj>* <smell_noun> _of|like_ <pronoun>* [<verb> <noun> {_of_ <noun>}*] [<verb> prep__*]",  # 1
    #
    # there came to the nostrils of father Thomas, a strange sharp smell, as of the sea.
    "[<verb> prep__*] <noun> {_of_ <noun>}* _,_* __DET* <pronoun>* <adj>* <smell_noun> _of|like_ [<noun> {_of_ <noun>}*]",  #  1
    #
    # the smell of dampness and of peat smoke from cottage chimneys filled the air
    "<smell_noun> _of_ <pronoun>* [<noun> {_and_ _of_ <noun>}*] _from_ <pronoun>* <noun> {_of_ <noun>}* [<verb> prep__*]",  #  1
    #
    # a yielding surface of leaf-mould, which sent up a warm smell
    "[<noun> {_of_ <noun>}*] _,_* __DET* [<verb> prep__*] __DET* <pronoun>* <adj>* <smell_noun>",  # 1
    #
    # patches of lily of the valley filled the air with fragrance
    "[<noun> {_of_ <noun>}*] [_filled_] _the_ _air_ _with_ <smell_noun>",  # 1
    #
    # the poplars covered with dew, filled the air with soft fragrance
    # "<noun> {_of_ <noun>}* _,_ <verb> prep__* <noun> _,_ [<verb> prep__*]",  # 1 Failed validation p=0
    #
    # [the roses] already inclined to droop [added] their fragrance
    # "<noun> {_of_ <noun>}* _,_* <verb> {prep__ <verb>}* _,_* [<verb> prep__*]",  # 1 Failed validation, p=0.1
    #
    # the rich aroma [distilled from] the [creamy hearts of roman hyacinths]
    # a truly celestial aroma [was given off by] the [fragrant pots of tea]
    "<smell_noun> __DET* [<verb> prep__*] <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    # the aroma of the [precious wine] seemed to [mingle] with
    # the aroma of new-sawn timber and sawdust began to be mingled  with...
    # "<smell_noun> _of_ __DET* [<noun> {_of_ <noun>}*] <verb> [prep__* <verb>]",  # 0  FAILED VALIDATION (precision = 0.67)
    #
    # a delicious aroma of [vanilla] [came to] Valiant's nostrils
    # the scents of spring, which stirred ....
    # the smell of a thousand potions again assailed lilly's nostrils
    "<smell_noun> _of_ <pronoun>* __DET* [__NUM* <noun> {_of_ <noun>}*] _,_* __DET* [<verb> prep__*]",  # 0  amended # 1
    #
    #
    # [carrying to] one's nostrils the aroma of the [Great North road]
    # a musty odor [rose] to his nostrils, the vigorous, pungent aroma of [raw cereal]
    "[<verb> prep__*] <pronoun>* <noun> _,_* __DET* <adj>* <smell_noun> _of_ [<noun> {_of_ <noun>}*]", # 0
    #
    # ****COMMON***
    # [lingered] the savoury aroma of [the duck mulligan]
    # [exhaling] the fragrant aroma of [the brain of the musk dear]
    # [impregnated with] the coarse aroma of [scented wood and malodorous flowers]
    "[<verb> prep__*] __DET* <adj>* <smell_noun> _of|like_ <pronoun>* [<noun> _of_ {<noun>}*]",  # 0
    #
    # had [rifled] some far-off garden of the aroma of [honeysuckle]
    # the air was [full] of the smell of [flowers]
    "[<verb> prep__*] <noun> _of_ __DET* <adj>* <pronoun>* <smell_noun> _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0  # 2 amended
    #
    # awakened to an aroma of coffee
    # eveloped by the delicate aroma of <noun>
    "[<verb> prep__*] __DET* <adj>* <smell_noun> _of_ <pronoun>* [<noun> {_of_ <noun>}*]",  # 0
    #
    # cake and cheese, and very fragrant coffee, whose aroma filled the entire house
    "[<noun> {_of_ <noun>}*] __DET* <adj>* <smell_noun> [<verb> prep__*]",  # 0
    #
    # [delicate lilac perfume] which [penetrated] the entire room
    "[<adj>* compound__] <smell_noun> __DET* [<verb> prep__*]",  # 0
    #
    # the perfume of the wisteria outside the open window came in sweetly
    "<smell_noun> _of_ <noun> {_of_ <noun>}* _,_* __DET* __ADP* <noun> _,_* <verb> prep__*",  # 2
    #
    # the smell of the roses, of poplars, and lilac came ...
    "<smell_noun> [{_of_ <noun> _,_*}* {_and_ <noun>}*] [<verb> prep__*]",  # 2
    #
    # the room was filled with the fragrance of violets
    #his nostrils pickup up the scent of ...
    "<noun> <verb> prep__* __DET* <smell_noun> _of_ <noun> {_of_ <noun>}*",  # 2
    #
    # from the hay came a sickly sweet, faintly troubling scent
    "_from_ <noun> <verb> __DET* <adj>* <smell_noun>",  # 2
    #
    # -----------------
    # <smelly_adj>
    # -----------------
    #
    # ------------------
    # <smells_noun>
    # ------------------
    #
    # whiffs of the freshness of evening were coming in ....
    "<smells_noun> _of_ <noun> {_of_ <noun>}* <verb> prep__*",  # 2
    #
    # the smells he had caught
    "<smells_noun> [{_of_ <noun>}]* <pronoun>* [<verb> prep__*]",  # 2
    #
    # ----
    # <smelled_verb>
    # ----
    #
    #  the lattic reeked of cheap tobacco
    "<noun> {_of_ <noun>}* [<verb>* <smelled_verb> <adv>* prep__*] <noun> {_of_ <noun>}*",  # 2
]

identification_patterns = [
    # -----
    # other
    # -----
    # the heavy fumes of incense rose up
    "_fumes_ _of_ _incense_ {_of_ <noun>}* __DET* <verb> prep__*",  # 1
    # ----
    # <smell_verb>
    # ----
    # i smell the fog that hung about the place
    "<smell_verb> <noun> {_of_ <noun>}* __DET* <verb> prep__*",  # 1
    # ------------------
    # <smells_verb>
    # ------------------
    #
    # ------------------
    # <smelling_verb>
    # ------------------
    # reeking with smoke and fog
    "<smelling_verb> _with_ <noun> {_of_ <noun>}*",  # 2
    # 
    # next came the strong smelling cheeses
    "<verb> prep__* __DET* <pronoun>* <adj>* <smelling_verb> <noun> {_of_ <noun>}*",  # 1
    #
    # ------------------
    # <smell_noun>
    # ------------------
    
    # shedding their delicate aroma
    # "<verb> <pronoun>* <adj> <smell_noun>",  # 0 (BASIC)
    #
    # where the oppresive smell came from
    # "<adj>* <smell_noun> verb> prep__*",  # 1 (BASIC)
    #
    # the stink of pitch and tallow
    # "<smell_noun> _of_ <noun>",  # 2  (BASIC)
    #
    # the smell of burning tobbaco came from
    "<adj>* <smell_noun> _of|like_ <pronoun>* [<verb> <noun> {_of_ <noun>}*] [<verb> prep__*]",  # 1
    #
    # there came to the nostrils of father Thomas, a strange sharp smell, as of the sea.
    "[<verb> prep__*] <noun> {_of_ <noun>}* _,_* __DET* <pronoun>* <adj>* <smell_noun> _of|like_ [<noun> {_of_ <noun>}*]",  #  1
    #
    # the smell of dampness and of peat smoke from cottage chimneys filled the air
    "<smell_noun> _of_ <pronoun>* [<noun> {_and_ _of_ <noun>}*] _from_ <pronoun>* <noun> {_of_ <noun>}* [<verb> prep__*]",  #  1
    #
    # a yielding surface of leaf-mould, which sent up a warm smell
    "<noun> {_of_ <noun>}* _,_* __DET* <verb> prep__* __DET* <pronoun>* <adj>* <smell_noun>",  # 1
    #
    # patches of lily of the valley filled the air with fragrance
    "<noun> {_of_ <noun>}* _filled_ _the_ _air_ _with_ <smell_noun>",  # 1
    #
    # the poplars covered with dew, filled the air with soft fragrance
    "<noun> {_of_ <noun>}* _,_ <verb> prep__* <noun> _,_ <verb> prep__*",  # 1
    #
    # [the roses] already inclined to droop [added] their fragrance
    "<noun> {_of_ <noun>}* _,_* <verb> {prep__ <verb>}* _,_* <verb> prep__*",  # 1
    #
    # the rich aroma [distilled from] the [creamy hearts of roman hyacinths]
    # a truly celestial aroma [was given off by] the [fragrant pots of tea]
    "<smell_noun> __DET* <verb> prep__* <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    # the aroma of the [precious wine] seemed to [mingle] with
    # the aroma of new-sawn timber and sawdust began to be mingled  with...
    "<smell_noun> _of_ __DET* <pronoun>* <noun> {_of_ <noun>}* <verb> prep__* <verb>",  # 0
    #
    # a delicious aroma of [vanilla] [came to] Valiant's nostrils
    # the scents of spring, which stirred
    "<smell_noun> _of_ <pronoun>* __DET* __NUM* <noun> {_of_ <noun>}* _,_* __DET* <verb> prep__*",  # 0  amended # 1
    #
    # [carrying to] one's nostrils the aroma of the [Great North road]
    # a musty odor [rose] to his nostrils, the vigorous, pungent aroma of [raw cereal]
    "<verb> prep__* <pronoun>* <noun> _,_* __DET* <adj>* <smell_noun> _of_ <noun> {_of_ <noun>}*",  # 0
    "<verb> prep__* <pronoun> _,_* __DET* <adj>* <smell_noun> _of_ <noun> {_of_ <noun>}*",  # 0
    #
    # ****COMMON***
    # [lingered] the savoury aroma of [the duck mulligan]
    # [exhaling] the fragrant aroma of [the brain of the musk dear]
    # [impregnated with] the coarse aroma of [scented wood and malodorous flowers]
    "<verb> prep__* __DET* <adj>* <smell_noun> _of|like_ <pronoun>* <noun> _of_ {<noun>}*",  # 0
    #
    # had [rifled] some far-off garden of the aroma of [honeysuckle]
    # the air was [full] of the smell of [flowers]
    # breathed the fragrance of thy bosom bare
    "<verb> prep__* <noun> _of_ __DET* <pronoun>* <adj>* <smell_noun> _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 0  # 2 amended 
    #
    # awakened to an aroma of coffee
    # eveloped by the delicate aroma of <noun>
    "<verb> prep__* __DET* <adj>* <smell_noun> _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    # cake and cheese, and very fragrant coffee, whose aroma filled the entire house
    "<noun> {_of_ <noun>}* __DET* <smell_noun> <verb> prep__*",  # 0
    #
    # [delicate lilac perfume] which [penetrated] the entire room
    "<adj>* compound__ <smell_noun> __DET* <verb> prep__*",  # 0
    #
    # the perfume of the wisteria outside the open window came in sweetly
    "<smell_noun> _of_ <noun> {_of_ <noun>}* _,_* __DET* __ADP* <noun> _,_* <verb> prep__*",  # 2
    #
    # the smell of the roses, of poplars, and lilac came ...
    "<smell_noun> [{_of_ <noun> _,_*}* {_and_ <noun>}*] [<verb> prep__*]",  # 2
    #
    # the room was filled with the fragrance of violets
    #his nostrils pickup up the scent of ...
    "<noun> <verb> prep__* __DET* <smell_noun> _of_ <noun> {_of_ <noun>}*",  # 2
    #
    # from the hay came a sickly sweet, faintly troubling scent
    "_from_ <noun> <verb> __DET* <adj>* <smell_noun>",  # 2
    #
    # ----
    # <smelly_adj>
    # ----
    #
    # a bouquet of aromatic herbs 
    # "<noun> _of_ <smelly_adj> <noun>",  # 2  (BASIC)
    #
    # rosemary-scented hills
    # "<noun> _-_ <smelly_adj> <noun>",  # 2 (BASIC)
    #
    # ----
    # <smells_noun>
    # ----
    # whiffs of the freshness of evening were coming in ....
    "<smells_noun> _of_ <noun> {_of_ <noun>}* <verb> prep__*",  # 2
    #
    #
    # the smells he had caught
    "<smells_noun> {_of_ <noun>}* <pronoun>* <verb> prep__*",  # 2
    #
    # foul smells arose and forced their way across the broad yellow beams like...
    "<adj>* <smells_noun> <verb> prep__*",  # 1
    #
    #
    
    # ----
    # <smelled_verb>
    # ----
    #
    #  the lattic reeked of cheap tobacco
    "<noun> {_of_ <noun>}* <verb>* <smelled_verb> <adv>* prep__* <noun> {_of_ <noun>}*",  # 2

]
