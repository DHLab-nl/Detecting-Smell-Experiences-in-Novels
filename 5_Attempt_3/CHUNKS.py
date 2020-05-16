# later definitions can reference earlier definitions
chunks = {

    #
    "<adj>": "{_and|,|or|-_* __ADJ+ _and|,|or|-_*}+",
    # the tall, dark and handsome
    #
    "<adv>": "__ADV+ {_and|,|or_ __ADV}*",
    # loadly and annoyingly
    #
    "<aux>": "<adv>* __AUX neg__* <adv>* {_and|,|or_ <adv>*}*",
    # really can very clearly and easily
    #
    "<verb>": "<aux>*  <adv>* __VERB <adv>* {_and|,|or_ <aux>* <adv>* __VERB <adv>*}*",
    # loadly and raucously singing, laughing and dancing wildly
    #
    "<prep>": "prep__ det__*",
    # with the , of the , in the, of
    #
    "<noun>": "{_and|,|or_* det__* poss__* __PART* <adj>* compound__* _-_* __NOUN|PROPN+}+",
    # "<noun>": "det__* poss__* __PART* <adj>* compound__* _-_* __NOUN|PROPN+ {_and|,|or_* det__* <adj>* compound__* _-_* __NOUN|PROPN+}*",
    # green, mottled tree-bark and pale roots of the tree
    #
    "<pronoun>": "{_and|,|or_* det__* poss__* __PART* <adj>* compound__* _-_* __PRON}+",
    #
    # "<subj>": "det__* <adj>* compound__* _-_* subj__ <prep>* {_and|,|or_* det__* <adj>* compound__* _-_* conj__}*",
    "<smell_noun>": "det__* poss__* __PART* <adj>* compound__* _-_* _aroma|bouqet|fragance|niff|perfume|musk|petrichor|odour|pong|pungency|redolence|reek|ripeness|savour|scent|stench|smell|sniff|stink|waft|whiff_NOUN",
    "<smells_noun>": "det__* poss__* __PART* <adj>* compound__* _-_* _aromas|fragrances|odours|perfumes|pongs|scents|smells|whiffs_NOUN",
    "<smells_verb>": "_pongs|reeks|smells|stinks|sniffs|stinks_VERB",
    "<smell_verb>": "_smell|reek|pong_VERB",
    "<smelled_verb>": "_smelled|smelt|scented|stank|sniffed|ponged|reeked_VERB",
    "<smelling_verb>": "_smelling|stinking|sniffing|ponging|reeking|reeking_VERB", 
    "<smelly_adj>": "_aromatic|fetid|foetid|odorous|fragranced|frowsty|fusty|malodorous|musky|musty|perfumed|piny|piney|pungent|putrid|redolent|ripe|scented|smelly|stinky|whiffy_ADJ",
    #
}
