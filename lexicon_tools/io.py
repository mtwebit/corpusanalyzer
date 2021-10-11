#!/usr/bin/python3

import json
import os
import sys, traceback
from .build import lexicon_export, lexicon_import
from collections import OrderedDict

def lexicon_load(lexdir) -> map:
    lexicon = {}
    if os.path.isdir(lexdir):
        for lexfile in os.listdir(lexdir):
            if '.json' in lexfile:
                with open(lexdir + "/" + lexfile, 'r', errors='replace') as fp:
                    try:
                        lexdata = json.load(fp)
                        lexicon_import(lexicon, lexdata)
                    except KeyboardInterrupt:
                        exit()
                    except OSError:
                        print(f"OS error while reading lexicon file {lexfile!r}.")
                        exit()
                    except:
                        print(f"Invalid lexicon file {lexfile!r}, ignoring.")
                        traceback.print_exc(file=sys.stdout)
                        exit()

        print(f"Lexicon loaded from {lexdir!r}.")
    return lexicon

def lexicon_save(lexdir, lexicon, sortkey='_occurrences'):
    if not os.path.isdir(lexdir):
        print(f"Creating lexicon directory {lexdir}.")
        os.mkdir(lexdir)

    lex_by_headword = lexicon_export(lexicon)

    print(f"Dumping the lexicon sorted by {sortkey} into {lexdir}/lexicon.json.")
    sortedlex = OrderedDict(sorted(lex_by_headword.items(), key=lambda headword: headword[1][sortkey], reverse=True))
    with open(lexdir + '/lexicon.json', 'w', errors='replace') as fp:
        json.dump(sortedlex, fp, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))

    print(f"Dumping the headwords and tokens sorted by number of token forms into {lexdir}/headwords.txt.")
    sortedlex = OrderedDict(sorted(lex_by_headword.items(), key=lambda headword: headword[1]['_wordforms'], reverse=True))
    with open(lexdir + '/headwords.txt', 'w', errors='replace') as fp:
        for headword, data in sortedlex.items():
            tokenlist = []
            for wordform in data.values():
                if type(wordform) is dict:
                    tokenlist += wordform.keys()
            fp.write(headword + " " + " ".join(tokenlist) + os.linesep)
