# copy of original, extraction patterns removed
# <smell_noun> adapted to <smells_noun>

identification_patterns = [
     # and inhale the sweet breath of autumn, which was borne upon gentle gales
    "<adj>* _breath|breaths_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # the soft warm breeze washes in dark fruit, dark flowers...
    "<adj>* _breeze_ _washes_ _in_ <pronoun>* <noun> {_of_ <noun>}*", # 1
    #
    #leaving a faint exhalation of scent and pwoer and delicate perfumes
    "<adj>* _exhalation|exhalations_ _of_ <noun> {_of_ <noun>}*",  # 2
    #
    # the air was laden with (the smell of) <noun>
    "<adj>* <noun> _was|is_ _laden_ _with_ {__DET* <smell_noun> _of_}+ <pronoun>* <noun> {_of_ <noun>}*", # 2
    "<adj>* _air_ _was|is_ _laden_ _with_ {__DET* <smell_noun> _of_}+ <pronoun>* <noun> {_of_ <noun>}*", # 2 POST PROCESS
    #
    # the mild air, sweet with fading leaves and bracken
    "<noun> {_of_ <noun>}* _,_ _sweet_ _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 3
    "_air_* _,_ _sweet_ _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 3
    #
    # sweet as a rose's breath
    "<adj>* _as_ <pronoun>* <noun> {_of_ <noun>}* _breath_",  # 1

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
    #-----
    # the sweet-smelling quince
    "<adv> _-_* <smelling_verb> <noun>",  # 1
    #
    # smelling of the clay
    "<adv>* <smelling_verb> <adv>* _of|like_ <noun>",  # 2
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
    "<noun> _was|were|is_ <smelly_adj> _with_ <pronoun>* <noun> {_of_ <noun>}*", # 1
    #
    # "<noun> _was|were|is_ _sweet_ _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 1 SEE OTHERS
    #
    # the air, fragrant with incense smoke
    "<noun> _,_* <smelly_adj> _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 1 
    #
    # with sweet scented, many coloured blossoms, that gave promise of delicios fruit
    "<adj>* <smelly_adj> _,_* <pronoun>* <noun> _that_ _gave|gives_ __DET* _promise_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # The pungent stifling smoke of powder
    "<adj>* <smelly_adj> <adj>* <noun> _of|like_ <noun> {_of_ <noun>}*",  # 1
    #
    # nearby rosemary-scented hills
    "<noun> _-_ <smelly_adj> <noun> {_of_ <noun>}*",  # 2
    #
    #----
    # <smells_noun>
    #----
    # the markishley sweet scents of the grass and flowers
    "<adj>* <smells_noun> _,_* _of|like_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    # smells as strong of brandy
    "<smells_noun> _as_ <adj> _of|like_ <noun> {_of_ <noun>}*",  # 1
    #
    # The air was exquisitely fragrant with earth and flower smells
    "<smells_verb> _with_ <noun> <smells_noun>",  # 2
    

    #----
    # <smell_noun>
    #----

    "<adj> <smell_noun>",  # 0 (BASIC)
    #
    # perfumed with a [delightful forest] aroma
    "compound__ _-_* <smell_noun>",  # 0 (BASIC)
    "<adj>* compound__ <smell_noun>",  # 0
    #
    # Never had an aroma been so sweet, so pervasive
    "<smell_noun> _been_* _so_ <adj>",  # 0
    "<smell_noun> <verb> prep__* <adj>",  # POST_PROCESSING
    #
    # the warm aroma of multitudinous exotics
    "<adj>* <smell_noun> _,_* _of|like_ <pronoun>* <noun> {_of_ <noun>}*",  # 0 amended PP
    #
    #what a truly a truly celestial aroma was given off by the fragrant pots of tea
    "<adj>* <smell_noun> _was_* _given_ _off_ _by_ <pronoun>* <noun> {_of_ <noun>}*",  # 0 amended PP
    "<adj>* <smell_noun> <verb> prep__* <pronoun>* <noun> {_of_ <noun>}*",  # POST_PROCESSING
    #
    # the cool, heavy aroma which one associates with the night
    "<adj>* <smell_noun> {_which_ _one_ _associates_}* _associated_* _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 0 amended PP
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
    "<adj>* <smell_noun> <verb> <noun> {_of_ <noun>}*",  # PP
    #
    # that aroma that suggested [a Sunday-school Christmas festival]
    # "<adj>* <smell_noun> {_that_ _suggested_}* _suggesting_* <pronoun>* <noun> {_of_ <noun>}*", # 0  Turned Off 0.75 precision
    #
    # the whitish eye-lashes, forceful freckles, and pungest aroma usually allied to [reddish hair]
    "<adj>* <smell_noun> _usually_ _allied_ _to_ <pronoun>* <noun> {_of_ <noun>}*", # 0
    #
    # the rich aroma distilled from [the creamy hearts of Roman hyacinths]
    "<adj>* <smell_noun> <verb>* _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    # the strong sunlight was an odour in his nostrils
    "<adj>* <noun> _was|is_ <smell_noun>",  # 1 amended PP
    #
    # He audaciously draws me by the hair to quaff the sweet wine of his breath, inhaled by him when he watered his favourite bakul-flowers.
    "<adj>* _wine_ _of|like_ <pronoun>* <noun> {_of_ <noun>}*",  # 1 amended PP
    #
    #a most delicious scent, which he found came from the the smell blossoms of the trees. 
    "<adj>* <smell_noun> _,_* _which_ _he_* _found_* _came_ _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 1
    #
    #There is a strange unwholesome smell upon the room, like mildewed corduroys....
    "<adj>* <smell_noun> {_upon_ _the_ _room_}* _,_* _of|like_ <pronoun>* <noun> {_of_ <noun>}*",  # 1 amended PP
    #
    #the sweet violets lent fragrance
    "<adj>* <noun> _lent_ <smell_noun>",  # 1
    #
    # the green leaves exhaled a sweet and refreshing fragrance
    "<noun> _exhaled_ <adj> <smell_noun>",  # 1
    #
    # smells as strong of brandy
    "<smell_noun> _as_ <adj> _of|like_ <noun>",  # 1 amended PP
    #
    # A subtle fragrance like that of sun-dried seaweed
    "<adj>* <smell_noun> _of|like_ {_that_ _of_}* <noun> {_of_ <noun>}*",  # 1 amended PP
    #
    # the <noun> gave out a strong scent
    "<noun> {_of_ <noun>}* _gave|giving_ _out_ __DET* <adj>* <smell_noun>",  # 1 amended PP
    #
    # the half open buds upon the trees shed there sweet perfume
    "<noun> {_of|upon_ <noun> }+ _shed|shedding_ <pronoun>* <adj>* <smell_noun>",  # 2 amended PP
    #
    #faint smell of putrifying bones
    #faint sweet smell of burning cedar
    "<adj>* <smell_noun> _of|like_ __DET* <pronoun>* <verb> <noun> {_of_ <noun>}*",  # 2
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
    "<noun> {_of_ <noun>}* _was_* _filled_ _with_ __DET* <adj>* <smell_noun> _of_ <noun> {_of_ <noun>}*",  # 3 amended PP
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
    "<smelled_verb> <adv>* _of|like_ __DET* <adj>* <pronoun>* <noun>",  # 2
    #
    # the mounains perfumed with flowers from a valley of roses
    "<smelled_verb> <adv>* _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 2
    #
    # ------------------
    # <smells_verb>
    # ------------------
    # the tea smells delicisously
    "<noun> {_of_ <noun>}* <smells_verb> <adv>",  #2 BASIC
    #
    # the town smells heartliy of cattle, sheep and malt
    "<smells_verb> <adv>* _of|like_ <noun> {_of_ <noun>}*",  # 2 amended PP
    #
    "<adj>* <smells_noun> _from_ __DET* <pronoun>* <verb>* <noun> {_of_ <noun>}*",  # 3

    "<adj> <smells_noun>", # POST_PROCESSING
    #POST_PROCESSING
    # perfumed with a [delightful forest] aromaPOST_PROCESSING
    "compound__ _-_* <smells_noun>",  # 0 (BASIC)POST_PROCESSING
    "<adj>* compound__ <smells_noun>",  # 0POST_PROCESSING
    #POST_PROCESSING
    # Never had an aroma been so sweet, so pervasivePOST_PROCESSING
    "<smells_noun> _been_* _so_ <adj>",  # 0POST_PROCESSING
    "<smells_noun> <verb> prep__* <adj>",  # POST_PROCESSINGPOST_PROCESSING
    #POST_PROCESSING
    # the warm aroma of multitudinous exoticsPOST_PROCESSING
    "<adj>* <smells_noun> _,_* _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    #POST_PROCESSING
    #what a truly a truly celestial aroma was given off by the fragrant pots of teaPOST_PROCESSING
    "<adj>* <smells_noun> _was_* _given_ _off_ _by_ <pronoun>* <noun> {_of_ <noun>}*",  # 0POST_PROCESSING amended PP
    "<adj>* <smells_noun> <verb> prep__* <pronoun>* <noun> {_of_ <noun>}*",  # POST_PROCESSINGPOST_PROCESSING
    #POST_PROCESSING
    # the cool, heavy aroma which one associates with the nightPOST_PROCESSING
    "<adj>* <smells_noun> {_which_ _one_ _associates_}* _associated_* _with_ <pronoun>* <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    #POST_PROCESSING
    # that [<adj>] aroma in which there is a foretaste of winePOST_PROCESSING
    "<adj>* <smells_noun> _in_ _which_ _there_ _is_ <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    #POST_PROCESSING
    # the <adj> smell from his great rubber coatPOST_PROCESSING
    "<adj>* <smells_noun> _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    #POST_PROCESSING
    #the fragrance breathed from the roses, gardeniasPOST_PROCESSING
    "<adj>* <smells_noun> <verb> _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 1POST_PROCESSING
    # Amidst the heavy exhilations of these, a Parmesan set a spicy aroma.POST_PROCESSING
    "<noun> {_of_ <noun>}* _set_ _a_ <adj>* <smells_noun>",  # 0POST_PROCESSING
    #POST_PROCESSING
    # the male aroma of him, a mixture of cigar smoke, bay rum and freshly washed handsPOST_PROCESSING
    "<adj>* <smells_noun> _of|like_ <pronoun> _,_ <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    "<adj>* <smells_noun> _of|like_ <pronoun>* <noun> _,_ <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    #POST_PROCESSING
    # whose aroma seemed a panting breathPOST_PROCESSING
    "<adj>* <smells_noun> _seemed_ <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    #POST_PROCESSING
    # that aroma that suggested [a Sunday-school Christmas festival]POST_PROCESSING
    "<adj>* <smells_noun> _that_ _suggested_ <pronoun>* <noun> {_of_ <noun>}*", # 0POST_PROCESSING
    #POST_PROCESSING
    # the whitish eye-lashes, forceful freckles, and pungest aroma usually allied to [reddish hair]POST_PROCESSING
    "<adj>* <smells_noun> _usually_* _allied_ _to_ <pronoun>* <noun> {_of_ <noun>}*", # 0POST_PROCESSING
    #POST_PROCESSING
        # the rich aroma distilled from [the creamy hearts of Roman hyacinths]POST_PROCESSING
    "<adj>* <smells_noun> <verb>* _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 0POST_PROCESSING
    #POST_PROCESSING
    "<adj>* _breeze_ _washes_ <pronoun>* <noun> {_of_ <noun>}*",  # 1POST_PROCESSING
    #POST_PROCESSING
    #and inhale the sweet breath of autumn, which was borne upon gentle galesPOST_PROCESSING
    "<adj>* _breath|breaths_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1POST_PROCESSING
    #POST_PROCESSING
    # sweet as rose's breathPOST_PROCESSING
    "<adj>* _as_ <pronoun>* <noun> {_of_ <noun>}* _breath_",  # 1POST_PROCESSING
    #POST_PROCESSING
    # the strong sunlight was an odour in his nostrilsPOST_PROCESSING
    "<adj>* <noun> _was_ <smells_noun>",  # 1POST_PROCESSING
    #POST_PROCESSING
    # He audaciously draws me by the hair to quaff the sweet wine of his breath, inhaled by him when he watered his favourite bakul-flowers.POST_PROCESSING
    "<adj>* _wine_ _of_ <pronoun>* <noun> {_of_ <noun>}*",  # 1POST_PROCESSING
    #POST_PROCESSING
    #a most delicious scent, which he found came from the the smell blossoms of the trees. POST_PROCESSING
    "<adj>* <smells_noun> _,_* _which_ _he_* _found_* _came_ _from_ <pronoun>* <noun> {_of_ <noun>}*",  # 1POST_PROCESSING
    #POST_PROCESSING
    #There is a strange unwholesome smell upon the room, like mildewed corduroys....POST_PROCESSING
    "<adj>* <smells_noun> {_upon_ _the_ _room_}* _,_* _like_ <pronoun>* <noun> {_of_ <noun>}*",  # 1POST_PROCESSING
    #POST_PROCESSING
    #the sweet violets lent fragrancePOST_PROCESSING
    "<adj>* <noun> _lent_ <smells_noun>",  # 1POST_PROCESSING
    #POST_PROCESSING
    # the green leaves exhaled a sweet and refreshing fragrancePOST_PROCESSING
    "<noun> _exhaled_ <adj> <smells_noun>",  # 1POST_PROCESSING
    #POST_PROCESSING
    # smells as strong of brandyPOST_PROCESSING
    "<smells_noun> _as_ <adj> _of_ <noun>",  # 1POST_PROCESSING
    #POST_PROCESSING
    # A subtle fragrance like that of sun-dried seaweedPOST_PROCESSING
    "<adj>* <smells_noun> _like_ {_that_ _of_}* <noun> {_of_ <noun>}*",  # 1POST_PROCESSING
    #POST_PROCESSING
    # the <noun> gave out a strong scentPOST_PROCESSING
    "<noun> {_of_ <noun>}* _gave|give_ _out_ __DET* <adj>* <smells_noun>",  # 1POST_PROCESSING
    #POST_PROCESSING
    # the half open buds upon the trees shed there sweet perfumePOST_PROCESSING
    "<noun> {_of|upon_ <noun> }+ _shed|shedding_ <pronoun>* <adj>* <smells_noun>",  # 2POST_PROCESSING
    #POST_PROCESSING
    #faint smell of putrifying bonesPOST_PROCESSING
    #faint sweet smell of burning cedarPOST_PROCESSING
    "<adj>* <smells_noun> _of|like_ __DET* <pronoun>* <verb> <noun> {_of_ <noun>}*",  # 2POST_PROCESSING
    #POST_PROCESSING
    # a yielding surface of leaf-mould, which sent up a warm smellPOST_PROCESSING
    "<noun> {_of_ <noun>}* _,_* __DET* _sent_ _up_ <adj>* <smells_noun>",  # 2POST_PROCESSING
    #POST_PROCESSING
    # heavy with the smell of freshly turned soilPOST_PROCESSING
    "<adj> _with_ __DET* <pronoun>* <smells_noun> _of_ <pronoun>* <verb> <noun> {_of_ <noun>}*",  # 2POST_PROCESSING
    #POST_PROCESSING
    # A perfume [heavy] as [incense], sweet as sandlewoodPOST_PROCESSING
    "<smells_noun> <adj> _as_ <noun> {_of_ <noun>}*",  # 3POST_PROCESSING
    "<smells_noun> <adj> _as_ <noun> {_of_ <noun>}* _and|,|or_* <adj>* _as_ <noun> {_of_ <noun>}*",  # 3POST_PROCESSING
    #POST_PROCESSING
    # the air was filled with the sweet odor of balsam, spruce and cedarPOST_PROCESSING
    "<noun> {_of_ <noun>}* _was_ _filled_ _with_ __DET* <adj>* <smells_noun> _of_ <noun> {_of_ <noun>}*",  # 3POST_PROCESSING
    


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
    "<smelling_verb> _with|of|like_ <noun> {_of_ <noun>}*",  # 2 amended PP
    # 
    # next came the strong smelling cheeses
    "<verb> prep__* __DET* <pronoun>* <adj>* <smelling_verb> <noun> {_of_ <noun>}*",  # 1
    #
    # ------------------
    # <smell_noun>
    # ------------------
    
    # shedding their delicate aroma
    "<verb> <pronoun>* <adj>* <smell_noun>",  # 0 (BASIC)
    #
    # where the oppresive smell came from
    "<adj>* <smell_noun> <verb> prep__*",  # 1 (BASIC)
    #
    # the stink of pitch and tallow
    "<smell_noun> _of|like_ <noun>",  # 2  (BASIC) amended PP
    #
    # the smell of burning tobbaco came from
    "<adj>* <smell_noun> _of|like_ <pronoun>* [<verb> <noun> {_of_ <noun>}*] [<verb> prep__*]",  # 1 amended PP
    #
    # there came to the nostrils of father Thomas, a strange sharp smell, as of the sea.
    "[<verb> prep__*] <noun> {_of_ <noun>}* _,_* __DET* <pronoun>* <adj>* <smell_noun> _of|like_ [<noun> {_of_ <noun>}*]",  #  1
    #
    # the smell of dampness and of peat smoke from cottage chimneys filled the air
    "<smell_noun> _of|like_ <pronoun>* [<noun> {_and_ _of|like_ <noun>}*] <verb>* _from_ <pronoun>* <noun> {_of_ <noun>}* [<verb> prep__*]",  #  1 amended PP
    #
    # a yielding surface of leaf-mould, which sent up a warm smell
    "<noun> {_of_ <noun>}* _,_* __DET* <verb> prep__* __DET* <pronoun>* <adj>* <smell_noun>",  # 1
    #
    # patches of lily of the valley filled the air with fragrance
    "<noun> {_of_ <noun>}* _filled_ _the_ _air_ _with_ <smell_noun>",  # 1
    "<noun> {_of_ <noun>}* _,_ <verb> prep__* <noun> _,_ <verb> prep__*",  # 1
    #
    # [the roses] already inclined to drop [added] their fragrance
    # "<noun> {_of_ <noun>}* _,_* <verb> {prep__ <verb>}* _,_* <verb> prep__*",  # 1
    #
    # the rich aroma [distilled from] the [creamy hearts of roman hyacinths]
    # a truly celestial aroma [was given off by] the [fragrant pots of tea]
    "<smell_noun> __DET* <verb> prep__* <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    # the aroma of the [precious wine] seemed to [mingle] with
    # the aroma of new-sawn timber and sawdust began to be mingled  with...
    "<smell_noun> _of|like_ __DET* <pronoun>* <noun> {_of_ <noun>}* <verb> prep__* <verb>",  # 0 amended PP
    #
    # a delicious aroma of [vanilla] [came to] Valiant's nostrils
    # the scents of spring, which stirred
    "<smell_noun> _of|like_ <pronoun>* __DET* __NUM* <noun> {_of_ <noun>}* _,_* __DET* <verb> prep__*",  # 0  amended # 1 amended PP
    #
    # [carrying to] one's nostrils the aroma of the [Great North road]
    # a musty odor [rose] to his nostrils, the vigorous, pungent aroma of [raw cereal]
    "<verb> prep__* <pronoun>* <noun> _,_* __DET* <adj>* <smell_noun> _of|like_ <noun> {_of_ <noun>}*",  # 0 amended PP
    "<verb> prep__* <pronoun> _,_* __DET* <adj>* <smell_noun> _of|like_ <noun> {_of_ <noun>}*",  # 0 amended PP
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
    "<verb> prep__* <noun> _of_ __DET* <pronoun>* <adj>* <smell_noun> _of|like_ <pronoun>* <noun> {_of_ <noun>}*",  # 0  # 2 amended 
    #
    # awakened to an aroma of coffee
    # eveloped by the delicate aroma of <noun>
    "<verb> prep__* __DET* <adj>* <smell_noun> _of|like_ <pronoun>* <noun> {_of_ <noun>}*",  # 0
    #
    # cake and cheese, and very fragrant coffee, whose aroma filled the entire house
    "<noun> {_of_ <noun>}* __DET* <smell_noun> <verb> prep__*",  # 0
    #
    # [delicate lilac perfume] which [penetrated] the entire room
    "<adj>* compound__ <smell_noun> __DET* <verb> prep__*",  # 0
    #
    # the perfume of the wisteria outside the open window came in sweetly
    "<smell_noun> _of|like_ <noun> {_of_ <noun>}* _,_* __DET* __ADP* <noun> _,_* <verb> prep__*",  # 2 amended PP
    #
    # the smell of the roses, of poplars, and lilac came ...
    "<smell_noun> [{_of|like_ <noun> _,_*}* {_and_ <noun>}*] [<verb> prep__*]",  # 2 amended PP
    #
    # the room was filled with the fragrance of violets
    #his nostrils pickup up the scent of ...
    "<noun> <verb> prep__* __DET* <smell_noun> _of|like_ <noun> {_of_ <noun>}*",  # 2 amended PP
    #
    # from the hay came a sickly sweet, faintly troubling scent
    "_from_ <noun> <verb> __DET* <adj>* <smell_noun>",  # 2
    #
    # ----
    # <smelly_adj>
    # ----
    #
    # a bouquet of aromatic herbs 
    "<noun> _of_ <smelly_adj> <noun>",  # 2  (BASIC)
    #
    # rosemary-scented hills
    "<noun> _-_ <smelly_adj> <noun>",  # 2 (BASIC)
    #
    # ----
    # <smells_noun>
    # ----
    #
    # whiffs of the freshness of evening were coming in ....
    "<smells_noun> _of_ <noun> {_of_ <noun>}* prep__* <verb> prep__*",  # 2
    #
    # the smells he had caught
    "<smells_noun> {_of_ <noun>}* prep__* <pronoun>* <verb> prep__*",  # 2
    #
    # foul smells arose and forced their way across the broad yellow beams like...
    "<adj>* <smells_noun> <verb> prep__*",  # 1
    #
    # TRANSFERRED FORM SMELL_NOUN
    ## shedding their delicate aroma (POST PROCESSING)
    "<verb> <pronoun>* <adj>* <smells_noun>",  # 0 (BASIC) (POST PROCESSING)
    # (POST PROCESSING)
    # the stink of pitch and tallow (POST PROCESSING)
    "<smells_noun> _of|like_ <noun>",  # 2  (BASIC) (POST PROCESSING)
    # (POST PROCESSING)
    # the smell of burning tobbaco came from (POST PROCESSING)
    "<adj>* <smells_noun> _of|like_ <pronoun>* [<verb> <noun> {_of_ <noun>}*] [<verb> prep__*]",  # 1 (POST PROCESSING)
    # (POST PROCESSING)
    # there came to the nostrils of father Thomas, a strange sharp smell, as of the sea. (POST PROCESSING)
    "[<verb> prep__*] <noun> {_of_ <noun>}* _,_* __DET* <pronoun>* <adj>* <smells_noun> _of|like_ [<noun> {_of_ <noun>}*]",  #  1 (POST PROCESSING)
    # (POST PROCESSING)
    # the smell of dampness and of peat smoke from cottage chimneys filled the air (POST PROCESSING)
    "<smells_noun> _of_ <pronoun>* [<noun> {_and_ _of_ <noun>}*] _from_ <pronoun>* <noun> {_of_ <noun>}* [<verb> prep__*]",  #  1 (POST PROCESSING)
    # (POST PROCESSING)
    # a yielding surface of leaf-mould, which sent up a warm smell (POST PROCESSING)
    "<noun> {_of_ <noun>}* _,_* __DET* <verb> prep__* __DET* <pronoun>* <adj>* <smells_noun>",  # 1 (POST PROCESSING)
    # (POST PROCESSING)
    # patches of lily of the valley filled the air with fragrance (POST PROCESSING)
    "<noun> {_of_ <noun>}* _filled_ _the_ _air_ _with_ <smells_noun>",  # 1 (POST PROCESSING)
    # (POST PROCESSING)
    # the rich aroma [distilled from] the [creamy hearts of roman hyacinths] (POST PROCESSING)
    # a truly celestial aroma [was given off by] the [fragrant pots of tea] (POST PROCESSING)
    "<smells_noun> __DET* <verb> prep__* <pronoun>* <noun> {_of_ <noun>}*",  # 0 (POST PROCESSING)
    # (POST PROCESSING)
    # the aroma of the [precious wine] seemed to [mingle] with (POST PROCESSING)
    # the aroma of new-sawn timber and sawdust began to be mingled  with... (POST PROCESSING)
    "<smells_noun> _of|like_ __DET* <pronoun>* <noun> {_of_ <noun>}* <verb> prep__* <verb>",  # 0 (POST PROCESSING)
    # (POST PROCESSING)
    # a delicious aroma of [vanilla] [came to] Valiant's nostrils (POST PROCESSING)
    # the scents of spring, which stirred (POST PROCESSING)
    "<smells_noun> _of|like_ <pronoun>* __DET* __NUM* <noun> {_of_ <noun>}* _,_* __DET* <verb> prep__*",  # 0  amended # 1 (POST PROCESSING)
    # (POST PROCESSING)
    # [carrying to] one's nostrils the aroma of the [Great North road] (POST PROCESSING)
    # a musty odor [rose] to his nostrils, the vigorous, pungent aroma of [raw cereal] (POST PROCESSING)
    "<verb> prep__* <pronoun>* <noun> _,_* __DET* <adj>* <smells_noun> _of|like_ <noun> {_of_ <noun>}*",  # 0 (POST PROCESSING)
    "<verb> prep__* <pronoun> _,_* __DET* <adj>* <smells_noun> _of|like_ <noun> {_of_ <noun>}*",  # 0 (POST PROCESSING)
    # (POST PROCESSING)
    # ****COMMON*** (POST PROCESSING)
    # [lingered] the savoury aroma of [the duck mulligan] (POST PROCESSING)
    # [exhaling] the fragrant aroma of [the brain of the musk dear] (POST PROCESSING)
    # [impregnated with] the coarse aroma of [scented wood and malodorous flowers] (POST PROCESSING)
    "<verb> prep__* __DET* <adj>* <smells_noun> _of|like_ <pronoun>* <noun> _of_ {<noun>}*",  # 0 (POST PROCESSING)
    # (POST PROCESSING)
    # had [rifled] some far-off garden of the aroma of [honeysuckle] (POST PROCESSING)
    # the air was [full] of the smell of [flowers] (POST PROCESSING)
    # breathed the fragrance of thy bosom bare (POST PROCESSING)
    "<verb> prep__* <noun> _of_ __DET* <pronoun>* <adj>* <smells_noun> _of|like_ <pronoun>* <noun> {_of_ <noun>}*",  # 0  # 2 amended  (POST PROCESSING)
    # (POST PROCESSING)
    # awakened to an aroma of coffee (POST PROCESSING)
    # eveloped by the delicate aroma of <noun> (POST PROCESSING)
    "<verb> prep__* __DET* <adj>* <smells_noun> _of_ <pronoun>* <noun> {_of|like_ <noun>}*",  # 0 (POST PROCESSING)
    # (POST PROCESSING)
    # cake and cheese, and very fragrant coffee, whose aroma filled the entire house (POST PROCESSING)
    "<noun> {_of_ <noun>}* __DET* <smells_noun> <verb> prep__*",  # 0 (POST PROCESSING)
    # (POST PROCESSING)
    # [delicate lilac perfume] which [penetrated] the entire room (POST PROCESSING)
    "<adj>* compound__ <smells_noun> __DET* <verb> prep__*",  # 0 (POST PROCESSING)
    # (POST PROCESSING)
    # the perfume of the wisteria outside the open window came in sweetly (POST PROCESSING)
    "<smells_noun> _of|like_ <noun> {_of_ <noun>}* _,_* __DET* __ADP* <noun> _,_* <verb> prep__*",  # 2 (POST PROCESSING)
    # (POST PROCESSING)
    # the smell of the roses, of poplars, and lilac came ... (POST PROCESSING)
    "<smells_noun> [{_of|like_ <noun> _,_*}* {_and_ <noun>}*] [<verb> prep__*]",  # 2 (POST PROCESSING)
    # (POST PROCESSING)
    # the room was filled with the fragrance of violets (POST PROCESSING)
    #his nostrils pickup up the scent of ... (POST PROCESSING)
    "<noun> <verb> prep__* __DET* <smells_noun> _of|like_ <noun> {_of_ <noun>}*",  # 2 (POST PROCESSING)
    # (POST PROCESSING)
    # from the hay came a sickly sweet, faintly troubling scent (POST PROCESSING)
    "_from_ <noun> <verb> __DET* <adj>* <smells_noun>",  # 2 (POST PROCESSING)

    
    # ----
    # <smelled_verb>
    # ----
    #
    #  the lattic reeked of cheap tobacco
    "<noun> {_of_ <noun>}* <verb>* <smelled_verb> <adv>* prep__* <noun> {_of_ <noun>}*",  # 2

]
