"""Assemble annotations.json and notes.json.
Example: 
    $python3 get_annotations.py

Returns:
    Annotations.json
        # {"set0":
              # by-annotator dict of extracts/ annotations
        #     {
                  # list of annotator:extract dicts wrt. set
        #         "annotator1":
        #         [
                      # extract & annotations within extract
        #             (
                          index,
        #                 extract_text,
        #                 [(label, annotation),...]
        #             ),
        #             ...
        #         ],
        #         ...
        #     },
        #     ....

        # }
"""
import json
import os
# from tei_reader import TeiReader
# import xml.etree.ElementTree as ET
import sys

import regex


def main(argv):

    files = __get_files()  # {'set3:["file/location",...],...}

    # ITERATE OVER FILES AND EXTRACT ANNOTATION SPANS and notes

    annotations = {}
    notes = {}

    # {"set0":
    # by-annotator dict of extracts/ annotations
    #     {
    # list of annotator:extract dicts wrt. set
    #         "annotator1":
    #         [
    # extract & annotations within extract
    #             (
    #                 index,
    #                 extract,
    #                 [(label, annotation),...]
    #             ),
    #             ...
    #         ],
    #         ...
    #     },
    #     ....

    # }

    for set, files in files.items():

        annotations[set] = {}
        notes[set] = {}

        for annotator, file in files.items():

            annotations[set][annotator] = []

            # read in file, remove CRs - affect pattern matching
            with open(file, "r") as f:
                doc = f.read()
            doc = doc.replace("\n", "")

            # get a list of extracts (raw tei) wrt. current doc
            text = regex.findall(r"<text>(.*?)</text>", doc)[0]
            extracts = regex.findall(r"<p>(.*?)</p>", text)

            # append spans to spans {}
            for index, extract in enumerate(extracts):
                # get annotations
                annotations[set][annotator].append([__get_annotations(extract, index)])

                # get notes
                cleaned_extract, extract_notes = __get_notes(extract)
                if any(extract_notes):
                    notes[set][annotator] = [cleaned_extract, extract_notes]

    # OUPUT TO JSON

    # annotations
    with open("annotations.json", "w") as f:
        json.dump(annotations, f, indent=4, ensure_ascii=False)

    # notes
    with open("notes.json", "w") as f:
        json.dump(notes, f, indent=4)


def __get_notes(extract):
    """Retreive notes.
    """

    extract_notes = regex.findall(r"<span.*?resp=\"(.*?)\">(.*?)</span>", extract)
    cleaned_extract = regex.sub(r"<.*?>", "", extract)

    return cleaned_extract, extract_notes


def __get_annotations(extract, index):
    """Return (extract_free_of_annotations, [(annotation, span),...]) for an extract 
    """

    # collect (only) spans within extract
    # ([(span,label),...])
    extract_spans = regex.findall(r"<span.*?ana=\"#(\w)\">(.*?)</span>", extract)
    cleaned_extract = regex.sub(r"<.*?>", "", extract)

    return str(index), cleaned_extract, extract_spans


def __get_files():
    """Collect a dict of xml file locations by set.

    Returns:
        files: {"set0":["/set0/annotator1/set0.xml", ...], ...}
    """

    files = {}
    # iterate through subfolders in current folder
    for dir in sorted(os.listdir()):

        # only act on /directories
        if os.path.isdir(dir):

            # init. key
            if str(dir) not in files.keys():
                files[str(dir)] = {}

            # iterate through next layer of nested sub-folders
            for dir2 in os.listdir(dir):

                path = os.path.join(dir, dir2)  # "/dir/dir2"
                # iterate through .xml files in each sub-folder

                for file in os.listdir(path):
                    path2 = os.path.join(path, file)
                    files[str(dir)][str(dir2)] = path2

    return files


if __name__ == "__main__":
    main(sys.argv[1:])
