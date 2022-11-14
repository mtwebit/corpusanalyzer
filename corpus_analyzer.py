#!/usr/bin/python3

import importlib
from tqdm import tqdm
import os
import html     # html cleanup

# pip install pycld3
import cld3     # language identification


from nltk.probability import FreqDist
from nltk.util import ngrams
from .lexicon_tools.io import lexicon_save, lexicon_load
from .lexicon_tools.build import lexicon_add_token, lexicon_lookup

def corpus_analyzer(corpus, lexdir=False, outdir=False, ngramfile=False, ngramsize=2, tokenfile=False, debug=False):
    """[Performs various NLP tasks on the corpus]

    Args:
        corpus ([type]): [Array of {'doc': file, 'text': } maps.]
        lexdir (bool, optional): [load and extend a lexicon]. Defaults to False.
        outdir (bool, optional): [dump result files into this dir]. Defaults to False.
        ngramfile (bool, optional): [create an ngram file]. Defaults to False.
        ngramsize (int, optional): [ngram size]. Defaults to 2.
        debug (bool, optional): [print out some messages]. Defaults to True.
    """
    if not len(corpus): return()
    if lexdir:
        lexicon = lexicon_load(lexdir)
    else:
        lexicon = {}

    if outdir:
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
            if debug: print("Creating working dir '" + outdir + "'...")
        outdir = outdir.strip(' /') + '/'

    if debug: print("Analyzing the corpus.")
    if outdir:
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
            if debug: print("Creating working dir '" + outdir + "'...")
        outdir = outdir.strip(' /') + '/'

    if debug: print("Analyzing the corpus.")
    docs = { entry['doc']: '' for entry in corpus }
    paras = 0
    for entry in corpus:
        text = entry['text']
        docs[entry['doc']] += text
        paras += text.count("\n")

    # Detect the language and load the appropriate language tools
    lang = cld3.get_language(corpus[0]['text']).language
    if debug: print(f"Detected language: {lang}")
    if debug: print(f"Detected language: {lang}")
    try:
        langtools = importlib.import_module(f"corpusanalyzer.language_tools.{lang}")
    except (ImportError, AttributeError):
        print(f"Error: language {lang!r} not supported.")
        quit()

#    for word in langtools.tokenizer("studies studying cries cry books said receives received"):
#        print(f"{word} -> ", langtools.stemmer(word))
#    quit()

    docprogress = tqdm(docs.items())
    docprogress.set_description("Sentence segmentation")
    sentences = { id: langtools.segmenter(text) for id, text in docprogress }
#    for word in langtools.tokenizer("studies studying cries cry books said receives received"):
#        print(f"{word} -> ", langtools.stemmer(word))
#    quit()

    docprogress = tqdm(docs.items())
    docprogress.set_description("Sentence segmentation")
    sentences = { id: langtools.segmenter(text) for id, text in docprogress }
    all_sentences = [ sentence for doc in sentences.values() for sentence in doc]
    nrsentences = len(all_sentences)
    all_text = ''.join(all_sentences)
    if outdir:
        if debug: print(f"Dumping sentences into sentences.txt.")
        with open(outdir + "sentences.txt", 'w', errors='replace') as fp:
            for s in all_sentences:
                fp.write(s + os.linesep + os.linesep)
    if outdir:
        if debug: print(f"Dumping sentences into sentences.txt.")
        with open(outdir + "sentences.txt", 'w', errors='replace') as fp:
            for s in all_sentences:
                fp.write(s + os.linesep + os.linesep)

    tokens = []
    stems = []
    pbar = tqdm(all_sentences, total=nrsentences)
    pbar.set_description("Tokenizing and stemming")
    pbar.leave = True
    mintokenlen = 3     # tokens shorter than this will be excluded from the results
    transtable = str.maketrans(':^/+=_', '      ')    # clear these in any text
    mintokenlen = 3     # tokens shorter than this will be excluded from the results
    transtable = str.maketrans(':^/+=_', '      ')    # clear these in any text
    for sent in pbar:  # sentences
        # Replace certain characters in the input with space, then run the tokenizer
        for token in langtools.tokenizer(sent.translate(transtable).strip()):
            t = html.unescape(token.lower())
            # drop short tokens
            if len(t) < mintokenlen: continue
            # drop short tokens
            if len(t) < mintokenlen: continue
            tokens.append(t)
            # break     # skip stemming and lexicon assembly
            if lexdir: tokenstem = lexicon_lookup(lexicon, t)
            else: tokenstem = False
            if not tokenstem:       # No lexicon or not in the lexicon
                try:
                    tokenstems = langtools.stemmer(t)    # provides array of possible stems
                    if len(tokenstems) < 1: tokenstem = t
                    else: tokenstem = tokenstems[-1]    # usually the last is the best
                except:
                    tokenstem = t
            if not tokenstem:       # non-recognized word
                tokenstem = t
            if lexdir and not t in langtools.stop_words: lexicon_add_token(lexicon, t, tokenstem, sent)
            stems.append(tokenstem)
            if lexdir: tokenstem = lexicon_lookup(lexicon, t)
            else: tokenstem = False
            if not tokenstem:       # No lexicon or not in the lexicon
                try:
                    tokenstems = langtools.stemmer(t)    # provides array of possible stems
                    if len(tokenstems) < 1: tokenstem = t
                    else: tokenstem = tokenstems[-1]    # usually the last is the best
                except:
                    tokenstem = t
            if not tokenstem:       # non-recognized word
                tokenstem = t
            if lexdir and not t in langtools.stop_words: lexicon_add_token(lexicon, t, tokenstem, sent)
            stems.append(tokenstem)
        pbar.update(1)

    print(f"Corpus: {len(docs)} documents, {paras} paragraphs, {len(all_sentences)} sentences, {len(tokens)} tokens, {len(stems)} stemmed tokens and {len(all_text)} characters.")

    tokens_nonstop = [token for token in tokens if not token in langtools.stop_words]
    if tokenfile:
        print(f"Dumping token frequency distribution into {tokenfile}.")
        with open(tokenfile, 'w', errors='replace') as fp:
            for token, fr in FreqDist(tokens_nonstop).most_common():
                fp.write(f"{token}\t{fr}" + os.linesep)
    if tokenfile:
        print(f"Dumping token frequency distribution into {tokenfile}.")
        with open(tokenfile, 'w', errors='replace') as fp:
            for token, fr in FreqDist(tokens_nonstop).most_common():
                fp.write(f"{token}\t{fr}" + os.linesep)

    if ngramfile:
        print(f"Dumping {ngramsize}-gram frequency distribution into {ngramfile}.")
        ngs = list(ngrams(tokens_nonstop, ngramsize))
        with open(ngramfile, 'w', errors='replace') as fp:
            for ng, fr in FreqDist(ngs).most_common():
                fp.write(f"{ng}\t{fr}" + os.linesep)
    if ngramfile:
        print(f"Dumping {ngramsize}-gram frequency distribution into {ngramfile}.")
        ngs = list(ngrams(tokens_nonstop, ngramsize))
        with open(ngramfile, 'w', errors='replace') as fp:
            for ng, fr in FreqDist(ngs).most_common():
                fp.write(f"{ng}\t{fr}" + os.linesep)

    if lexdir:
        lexicon_save(lexdir, lexicon)

