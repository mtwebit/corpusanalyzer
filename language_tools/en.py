#!/usr/bin/python3

# pip install nltk
# python -m nltk.downloader stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nnsplit import NNSplit
from nltk.tokenize import ToktokTokenizer
from hunspell import Hunspell
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# pip install nnsplit
from nnsplit import NNSplit

# apt install hunspell hunspell-en
# pip install cyhunspell
from hunspell import Hunspell

#
# Choose language tools
#
import spacy

# TODO: https://github.com/dlt-rilmta/emtsv    emagyar, Java-based, Python-integration
# provides many tools for Hungarian language


# sentence segmenter
#
# Spacy
# spacy_segmenter = spacy.load('en_core_web_sm')
# If you need fast sentence segmentation without dependency parses, disable the parser use the senter component instead:
# spacy_segmenter.disable_pipe("parser")
# spacy_segmenter.enable_pipe("senter")
# segmenter = lambda x: [ s.text.rstrip() for s in spacy_segmenter(x).sents ]
#
# A classic
segmenter = PunktSentenceTokenizer().sentences_from_text
#
# TODO: https://github.com/notAI-tech/deepsegment   does not require punctuations and capitalisations but requires CUDA
# segmenter = DeepSegment('en').segment
#
# NNSplit
# segmenter = lambda x: [ str(sentence).rstrip() for split in NNSplit.load("en").split([x]) for sentence in split ]
#
# Evaluation
# text = "Automotive parts supplier Minda Industries Ltd., has acquired the location-tracking (telematics) hardware business of KPIT Engineering, which provides IT consulting and product engineering services to automakers, it said in a stock exchange filing. The retail chain operator recorded a revenue of ₹5,149 crore, a y-o-y jump of 13.5% over the same period last year. It reported a profit growth of 11% to ₹170 crore in the quarter ended 30 June. The transaction in Future Retail, follows a structured debt fundraise of close to $250 million in Biyani’s apparel retail business Future Lifestyle Fashions, which operates Central and Brand Factory. The funds were raised from PE firm Blackstone. Automotive parts supplier Minda Industries Ltd., has acquired the location-tracking (telematics) hardware business of KPIT Engineering, which provides IT consulting and product engineering services to automakers, it said in a stock exchange filing. Rubicon Technology Partners has agreed to make a majority investment in Cin7, a provider of cloud-based inventory management software and point-of-sale solutions. No financial terms were disclosed."
# text += "Navi Technologies Pvt. Ltd, the financial services company set up by Flipkart co-founder Sachin Bansal, has raised funding from mid-market private equity firm Gaja Capital and a number of individual investors."
# text += "NEW YORK & NEW DELHI--(BUSINESS WIRE)--Kemp, the leader in powering always-on application experience [AX], today announced it has acquired Lithops Technologies, a top developer of application networking and network security solutions and services based in New Delhi, India. The acquisition will further fuel the development of Kemp load balancer and AX products, while accelerating the company’s business development efforts across India"
# print(text)
# import json
# print(json.dumps(segmenter(text), sort_keys=False, indent=4, separators=(',', ': ')))
# quit()

#
# tokenizer
#
# TokTok works on sentence level, pretty fast
# tokenizer = ToktokTokenizer().tokenize
#mintokenlen = 3     # tokens shorter than this will be excluded from the results
#transtable = str.maketrans(':^/+=_', '      ')    # clear these in any text
#
# TODO: https://github.com/fnl/segtok
# Ezt használja a Flair is. Szegmentálni is tud.
#
# Spacy is much slower but it's better if you use it for other tasks
spacy_tokenizer = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "lemmatizer", "ner"])
tokenizer = lambda x: [str(token) for token in spacy_tokenizer(x)]
# print(tokenizer("Edelweiss Financial Services Limited Tuesday announced that it is selling a minority stake in wholly owned subsidiary Edelweiss Insurance Brokers Limited (EIBL) to US-based Arthur J. Gallagher & Co., a brokerage and risk management services firm."))

#
# stemmer
#
# pretty slow but better than any other stemmer present below
stemmer = Hunspell('en_US', system_encoding='UTF-8').stem

# others aren't soo goooood
# stemmer = lambda x: [ SnowballStemmer("english").stem(x), PorterStemmer().stem(x) ] + list(Hunspell('en_US', system_encoding='UTF-8').stem(x))

stop_words = stopwords.words('english')

print("English language tools loaded.")
