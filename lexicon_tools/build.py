#!/usr/bin/python3

# Lexicon structure
# headword - címszó
#   wordform1 - alakváltozat (ragozatlan szóalak, a címszó egyik írásmódja)
#       token11 - szóalak (ragozott alakváltozat)
#           sample111 - példamondat
#   wordform2
#       token21
#           sample211
# It is organized by tokens during runtime
# token
#   headword1
#       wordform, samples
#

# The lexicon is indexed by tokens to speed up headword lookup for a token
def lexicon_add_token(lexicon, headword, wordform, token, sample = '', headword_extra = '', sample_extra = '') -> None:
    # logging.debug(f"Adding {token} to {headword}")
    if not token in lexicon.keys():
        lexicon[token] = { headword: { '_extra': headword_extra, wordform: { sample: sample_extra } } }
        return
    if not headword in lexicon[token].keys():
        lexicon[token][headword] = { '_extra': headword_extra, wordform: { sample: sample_extra } }
        return
    if headword_extra != '':
        lexicon[token][headword]['_extra'] = headword_extra
    if not wordform in lexicon[token][headword].keys():
        lexicon[token][headword][wordform] = { sample: sample_extra }
        return
    lexicon[token][headword][wordform][sample] = sample_extra

def lexicon_lookup(lexicon, token):
    if token in lexicon.keys():
        return lexicon[token]
    return False

# Reconstructing the headword-based lexicon
def lexicon_export(lexicon):
    lexdata = {}
    for token, data in lexicon.items():
        for headword in data.keys():
            if not headword in lexdata.keys():
                lexdata[headword] = { '_occurrences': 0, '_wordforms': 0, '_tokenforms': 0, '_extra': data[headword]['_extra'] }
            for wordform in data[headword].keys():
                if wordform == "_extra": continue
                if not wordform in lexdata[headword].keys():
                    lexdata[headword][wordform] = { }
                    lexdata[headword]['_wordforms'] += 1
                # print(f"{headword}: {wordform}: {token}")
                if not token in lexdata[headword][wordform].keys():
                    lexdata[headword][wordform][token] = {}
                    lexdata[headword]['_tokenforms'] += 1
                lexdata[headword][wordform][token].update(data[headword][wordform])
                lexdata[headword]['_occurrences'] += len(data[headword][wordform])
            # TODO increase counters
    return lexdata

def lexicon_import(lexicon, lexdata):
    for headword, hwdata in lexdata.items():
        for wordform, wfdata in hwdata.items():
            if wordform[0] == "_": continue     # special keys start with _
            for token, samples in wfdata.items():
                for sample, sample_extra in samples.items():
                    lexicon_add_token(lexicon, headword, wordform, token, sample, headword_extra = hwdata['_extra'], sample_extra = sample_extra)
