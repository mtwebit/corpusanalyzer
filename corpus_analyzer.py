#!/usr/bin/python3

import importlib
from tqdm import tqdm
import html     # html cleanup
import cld3     # language identification
from nltk.probability import FreqDist
from nltk.util import ngrams
from .lexicon_tools.json import lexicon_save
from .lexicon_tools.build import lexicon_add_token

def corpus_analyzer(corpus, lex=False):
    lexicon = {}

    print("Loading and analyzing the corpus.")
    docs = { entry['doc']: '' for entry in corpus }
    paras = 0
    for entry in corpus:
        text = entry['text']
        docs[entry['doc']] += text
        paras += 1

    # Detect the language and load the appropriate language tools
    lang = cld3.get_language(corpus[0]['text']).language
    print(f"Detected language: {lang}")
    try:
        langtools = importlib.import_module(f"corpusanalyzer.language_tools.{lang}")
    except (ImportError, AttributeError):
        print(f"Error: language {lang!r} not supported.")
        quit()

    sentences = { id: langtools.segmenter(text) for id, text in docs.items() }
    all_sentences = [ sentence for doc in sentences.values() for sentence in doc]
    nrsentences = len(all_sentences)
    all_text = ''.join(all_sentences)

    tokens = []
    stems = []
    pbar = tqdm(all_sentences, total=nrsentences)
    pbar.set_description("Tokenizing and stemming")
    pbar.leave = True
    for sent in pbar:  # sentences
        # The ToktokTokenizer tokenizes sentences
        for token in langtools.tokenizer(sent.translate(langtools.transtable).strip()):
            t = html.unescape(token.lower())
            if len(t) < langtools.mintokenlen: continue
            tokens.append(t)
            # break     # skip stemming and lexicon assembly
            tokenstems = langtools.stemmer(t)
            if len(tokenstems) < 2:  # non-recognized word
                stems.append(t)
            else:
                if lex and not t in langtools.stop_words: lexicon_add_token(lexicon, t, tokenstems[0], sent)
                stems.append(tokenstems[0])  # the best guess
        pbar.update(1)

    print(f"Corpus: {len(docs)} documents, {paras} paragraphs, {len(all_sentences)} sentences, {len(tokens)} tokens, {len(stems)} stemmed tokens and {len(all_text)} characters.")

    tokens_nonstop = [token for token in tokens if not token in langtools.stop_words]
    print(f"---------- Most common tokens excluding stopwords:")
    print(FreqDist(tokens_nonstop).most_common(50))

    stems_nonstop = [token for token in stems if not token in langtools.stop_words]
    print(f"---------- Most common stemmed token excluding stopwords:")
    print(FreqDist(stems_nonstop).most_common(50))

    bigrams = list(ngrams(tokens_nonstop, 2))
    print(f"---------- Most common token bigrams:")
    print(FreqDist(bigrams).most_common(50))

    bigrams = list(ngrams(stems_nonstop, 2))
    print(f"---------- Most common stemmed token bigrams:")
    print(FreqDist(bigrams).most_common(50))

    if lex: lexicon_save(lex, lexicon)

