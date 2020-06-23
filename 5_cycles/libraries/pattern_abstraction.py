"""Functions to handle abstracted language patterns.
"""
import re

from CHUNKS import chunks


def convert_patterns(patterns, chunks=chunks):
    """Function to convert abstracted patterns to python patterns.
    Args:
        patterns (list): list of abstacted patterns to convert to python patterns wrt. spaCy parsed text.

            tokens: dep_text_pos
            e.g., det__ matches all determiners
                  _and_ matches all text instances of and
                  __NOUN matches all nouns
                  _smell_VERB matches the text smell, when used as a verb
                  _smell|fragrance|whiff_, matches or cases

            chunks:
            e.g., <noun>
                  chunks defined in CHUNKS.py can be referenced directly

            repetitions:
            *=zero or more, +=one or more
            e.g., det__ __ADJ* __NOUN, matches zero or more adjectives
                  det__ VERB __ADV+, matches one or more adverbs

            groups repetitions:
            {}* = zero or more, {}+=one or more
            e.g., det__ <noun> {_and|or|, <noun>}*

        chunks (list): 

    Returns:
        a list of python patterns

    Example
        det__* [__NOUN] {_and|,|or [__NOUN]}*
        Which would match, e.g., "the cats, dogs and antelopes", and any re.match object would return the __NOUN entries as re.match().groups()
    """

    output = []
    pattern_as_string = []
    for pattern in patterns:

        # replace chunks with abstracted patterns
        print(pattern)
        pattern = expand_chunks(pattern, chunks)

        python_pattern = []


        # convert each token to a python pattern
        blocks = [
            t
            for t in re.split(r"({|\[|}\*|}\+|\]\*|\]\+|\])|\s+", pattern)
            if t != "" and t is not None
        ]

        # iterate over blocks
        for block_index, block in enumerate(blocks):

            # reset for handling block *, +
            zero_or_more, one_or_more = False, False

            # handle brackets
            if block == "{":
                python_pattern.append("(?:")
                continue
            elif block == "}*":
                python_pattern.append(")*")
                continue
            elif block == "}+":
                python_pattern.append(")+")
                continue
            elif block == "[":
                python_pattern.append("(")
                continue
            elif block == "]":
                python_pattern.append(")")
                continue
            elif block == "]*":
                python_pattern.append(")*")
                continue
            elif block == "]+":
                python_pattern.append(")+")
                continue

            # handle *, + operators (record and remove)
            if block[-1] == "*":
                block = block[:-1]
                zero_or_more = True
            if block[-1] == "+":
                block = block[:-1]
                one_or_more = True

            # split into parse components and process
            dep, text, pos = block.split("_")
            if dep == "":
                dep = "\S+"
            if text == "":
                text = "\S+"
            if pos == "":
                pos = "\S+"

            # process | in dep, text or pos
            if "|" in dep:
                dep = "(?:" + dep + ")"
            if "|" in text:
                text = "(?:" + text + ")"
            if "|" in pos:
                pos = "(?:" + pos + ")"

            # implement *, +
            if zero_or_more:
                token_python = "(?:" + dep + "_" + text + "_" + pos + ")*"
            elif one_or_more:
                token_python = "(?:" + dep + "_" + text + "_" + pos + ")+"
            else:
                token_python = dep + "_" + text + "_" + pos

            python_pattern.append(token_python)

            # reset
            zero_or_more, one_or_more = False, False

        # append to output as string
        pattern_as_string = ""
        last_term = None
        for term in python_pattern:
            if last_term is None:
                pattern_as_string += term
            elif last_term in ["(", "(?:", "{"]:
                pattern_as_string += term
            elif term in ["}*", "}+", ")", ")*", ")+"]:
                pattern_as_string += term
            else:
                pattern_as_string += "\s*" + term
            last_term = term

        output.append(pattern_as_string)

    return output


def expand_chunks(pattern, chunks):
    """Replace <chunk> entries in pattern, with abstracted form.
       Capable of handling nested chunks, calling itself recursively

    Args:
        pattern (str): simplified sentence pattern

    Returns:
        'abstracted' pattern with all chunks expanded
    """
    # collect each 'block', i.e. potential chunk, in the pattern as a list
    #   replace chunk key with 'abstracted pattern' value
    blocks = []
    for block in re.split(r"\s+|(}\*|}\+|}|\]|{|\[)", pattern):

        if block is None or block == "":
            continue

        if block[0] == "<":
            if block[-1] == "*":
                blocks.append("{" + chunks[block[:-1]] + "}*")
            else:
                blocks.append(chunks[block])
        else:
            blocks.append(block)

    # collect blocks list into string, correctly ommitting spaces
    pattern_as_string = ""
    last_term = None
    for term in blocks:
        if last_term is None:
            pattern_as_string += term
        elif last_term in ["{", "\["]:
            pattern_as_string += term
        elif term in ["}*", "}+", "\]"]:
            pattern_as_string += term
        else:
            pattern_as_string += " " + term
        last_term = term

    # recursively re-run if expanded old chunks resulted in new chunks
    if "<" in pattern_as_string:
        return expand_chunks(pattern_as_string, chunks)
    else:
        return pattern_as_string


def to_chunks(extract, chunks):
    """
    Convert extract to strings of chuncks, where applicable.
    """

    # iterate from chunks, starting from highest level
    chunks_reversed = dict(reversed(list(chunks.items())))
    for chunk, chunk_definition in chunks_reversed.items():

        # convert abstracted pattern form to python patten
        chunk_as_python_pattern = convert_patterns([chunk_definition])[0]

        # Find the highest level (outermost branch) chunk, recursively do the
        # same for the remainder of the extract
        mo = regex.match(".*" + chunk_as_python_pattern + ".*", extract)

        if mo:

            # e.g., sub_extracts = [unmatched, matched, unmatched]
            sub_extracts = re.split("(" + chunk_as_python_pattern + ")", extract)
            sub_extracts = [s for s in sub_extracts if s != "" and s != None]

            # iterate through the sub extracts
            collected = []
            for sub_extract in sub_extracts:

                if regex.match(chunk_as_python_pattern, sub_extract):
                    collected.append(chunk)
                else:
                    collected.append(to_chunks(sub_extract.strip()))

            return " ".join(collected)

    # no match, then return unaltered extract
    return extract
