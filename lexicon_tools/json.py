import json
import os

def lexicon_load(file) -> map:
    if os.path.isfile(file):
        with open(file, 'r', errors='replace') as fp:
            try:
                data = json.load(fp)
            except:
                print("Invalid lexicon file {file!r}, ignoring.")
                return {}
        lexicon = { entry[0]: entry[1] for entry in data }
        return lexicon
    else:
        return {}

def lexicon_save(file, lexicon):
    lex_sorted = sorted(lexicon.items(), key=lambda headword: headword[1]['occurrences'], reverse=True)
    # print(json.dumps(lexicon, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': ')))
    with open(file, 'w', errors='replace') as fp:
        json.dump(lex_sorted, fp, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
