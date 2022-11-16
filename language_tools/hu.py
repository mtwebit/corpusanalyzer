#!/usr/bin/python3

# pip install nltk
# python -m nltk.downloader stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import ToktokTokenizer
from nltk.corpus import stopwords

# apt install hunspell hunspell-hu libhunspell-dev
# pip install cyhunspell
from hunspell import Hunspell

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
stemmer = Hunspell('hu_HU', system_encoding='UTF-8', hunspell_data_dir='/usr/share/hunspell/').stem

stop_words = stopwords.words('hungarian') + \
     [ 'mind', 'két', 'első', 'azaz']
     # ábra', 'látható', 'például', 'vesz', 'észre', 'lehetővé', 'tenni', 'lásd', 'fejezet', 'lásd', 'ily', 'módon' ]

print("Hungarian language tools loaded.")

print(stemmer("ébresztőt"))