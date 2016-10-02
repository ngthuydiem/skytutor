# Example: ./word2vec.py ~/workspace/word2vec/text8 ~/workspace/word2vec/questions-words.txt ./text8
import logging
import sys
import os
from numpy import seterr
from gensim import utils

logger = logging.getLogger(__name__)
MAX_WORDS_IN_BATCH = 10000


class WikiCorpus(object):
	"""Iterate over sentences from the "text8" corpus, unzipped from http://mattmahoney.net/dc/text8.zip ."""
	def __init__(self, fname, max_sentence_length=MAX_WORDS_IN_BATCH):
		self.fname = fname
		self.max_sentence_length = max_sentence_length

	def __iter__(self):
		# the entire corpus is one gigantic line -- there are no sentence marks at all
		# so just split the sequence of tokens arbitrarily: 1 sentence = 1000 tokens
		sentence, rest = [], b''
		with utils.smart_open(self.fname) as fin:
			while True:
				text = rest + fin.read(8192)  # avoid loading the entire file (=1 line) into RAM
				if text == rest:  # EOF
					sentence.extend(rest.split())  # return the last chunk of words, too (may be shorter/longer)
					if sentence:
						yield sentence
					break
				last_token = text.rfind(b' ')  # last token may have been split in two... keep for next iteration
				words, rest = (utils.to_unicode(text[:last_token]).split(),
							   text[last_token:].strip()) if last_token >= 0 else ([], text)
				sentence.extend(words)
				while len(sentence) >= self.max_sentence_length:
					yield sentence[:self.max_sentence_length]
					sentence = sentence[self.max_sentence_length:]

import argparse
from gensim.models.word2vec import Word2Vec

if __name__ == "__main__":
	logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
	program = os.path.basename(__file__)
			
	parser = argparse.ArgumentParser(description='Training parameters')
	parser.add_argument('--input', dest='input', type=str, required=True)
	parser.add_argument('--output', dest='output', type=str)
	parser.add_argument('--question', dest='question', type=str)
	 # word2vec model: cbow or skip-gram
	parser.add_argument('--algo', dest='algo', type=str, default='skip-gram') 
	# optimization technique: negative-sampling or hierarchical softmax
	parser.add_argument('--opt', dest='opt', type=str, default='negative-sampling')
	# number of threads: 1-32	
	parser.add_argument('--nthreads', dest= 'nthreads', type=int, default=8)	
	args = parser.parse_args()		
	logger.info("running %s", args)
	
	# variables to fix
	num_features = 300 # dimensionality of feature vectors
	num_negative_samples = 5 # number of noise words to draw for negative sampling (5-20)
	min_word_frequency = 5 # ignore all words with total frequency lower than this
		
	algo_bool = 1 if args.algo == 'skip-gram' else 0
	opt_bool = 1 if args.opt == 'negative-sampling' else 0	
	
	logger.info("--------------------Training--------------------")
	model = Word2Vec(WikiCorpus(args.input), size=num_features, min_count=min_word_frequency, 
		workers=args.nthreads, sg=algo_bool, hs=opt_bool, negative=num_negative_samples)
	
	if args.output:
		logger.info("--------------------Output Model--------------------")
		model.save(args.output + '.model')
		
	if args.question:
		logger.info("--------------------Validation--------------------")
		model.accuracy(args.question)
		
	logger.info("finished running %s", program)

