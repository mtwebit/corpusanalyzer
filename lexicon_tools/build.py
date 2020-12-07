def lexicon_add_token(lexicon, token, headword, sentence):
    # logging.debug(f"Adding {token} to {headword}")
    if headword in lexicon.keys():
        lexicon[headword]['occurrences'] += 1
        if token in lexicon[headword]['tokens'].keys():
            lexicon[headword]['tokens'][token].append(sentence)
        else:
            lexicon[headword]['tokens'][token] = [ sentence ]
    else:
        lexicon[headword] = { 'occurrences': 1, 'tokens': { token: [ sentence ] }}

