#!/usr/bin/python3

from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import ToktokTokenizer
from hunspell import Hunspell
from nltk.corpus import stopwords

#
# Choose language tools
#

# TODO: https://github.com/dlt-rilmta/emtsv    emagyar, Java-based, Python-integration
# provides many tools for Hungarian language


# sentence segmenter
# TODO: https://github.com/notAI-tech/deepsegment   does not require punctuations and capitalisations
segmenter = PunktSentenceTokenizer().sentences_from_text

# tokenizer, works on sentence level, really fast
tokenizer = ToktokTokenizer().tokenize
mintokenlen = 3     # tokens shorter than this will be excluded from the results
transtable = str.maketrans(':^/+=_', '      ')    # clear these in any text

# stemmer for Hungarian language, pretty slow but better than NLTK's Porter stemmer
stemmer = Hunspell('hu_HU', system_encoding='UTF-8').stem

stop_words = stopwords.words('hungarian') + \
     [ 'mind', 'két', 'első', 'azaz']
     # ábra', 'látható', 'például', 'vesz', 'észre', 'lehetővé', 'tenni', 'lásd', 'fejezet', 'lásd', 'ily', 'módon' ]

print("Hungarian language tools loaded.")