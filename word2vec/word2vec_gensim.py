# Example: ./word2vec.py ~/workspace/word2vec/text8 ~/workspace/word2vec/questions-words.txt ./text8
import logging
import sys
import os
from numpy import seterr
from gensim import utils

logger = logging.getLogger(__name__)
MAX_WORDS_IN_BATCH = 10000

class BrownCorpus(object):
	"""Iterate over sentences from the Brown corpus (part of NLTK data)."""
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for fname in os.listdir(self.dirname):
			fname = os.path.join(self.dirname, fname)
			if not os.path.isfile(fname):
				continue
			for line in utils.smart_open(fname):
				line = utils.to_unicode(line)
				# each file line is a single sentence in the Brown corpus
				# each token is WORD/POS_TAG
				token_tags = [t.split('/') for t in line.split() if len(t.split('/')) == 2]
				# ignore words with non-alphabetic tags like ",", "!" etc (punctuation, weird stuff)
				words = ["%s/%s" % (token.lower(), tag[:2]) for token, tag in token_tags if tag[:2].isalpha()]
				if not words:  # don't bother sending out empty sentences
					continue
				yield words

class Text8Corpus(object):
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


class LineSentence(object):
	"""
	Simple format: one sentence = one line; words already preprocessed and separated by whitespace.
	"""

	def __init__(self, source, max_sentence_length=MAX_WORDS_IN_BATCH, limit=None):
		"""
		`source` can be either a string or a file object. Clip the file to the first
		`limit` lines (or no clipped if limit is None, the default).

		Example::

			sentences = LineSentence('myfile.txt')

		Or for compressed files::

			sentences = LineSentence('compressed_text.txt.bz2')
			sentences = LineSentence('compressed_text.txt.gz')

		"""
		self.source = source
		self.max_sentence_length = max_sentence_length
		self.limit = limit

	def __iter__(self):
		"""Iterate through the lines in the source."""
		try:
			# Assume it is a file-like object and try treating it as such
			# Things that don't have seek will trigger an exception
			self.source.seek(0)
			for line in itertools.islice(self.source, self.limit):
				line = utils.to_unicode(line).split()
				i = 0
				while i < len(line):
					yield line[i : i + self.max_sentence_length]
					i += self.max_sentence_length
		except AttributeError:
			# If it didn't work like a file, use it as a string filename
			with utils.smart_open(self.source) as fin:
				for line in itertools.islice(fin, self.limit):
					line = utils.to_unicode(line).split()
					i = 0
					while i < len(line):
						yield line[i : i + self.max_sentence_length]
						i += self.max_sentence_length

import argparse
from gensim.models.word2vec import Word2Vec

if __name__ == "__main__":
	logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
	program = os.path.basename(__file__)
			
	parser = argparse.ArgumentParser(description='Training parameters')
	parser.add_argument('--input_file', dest='input', type=str, required=True)
	parser.add_argument('--output_file', dest='output', type=str)
	parser.add_argument('--question_file', dest='question', type=str)
	 # word2vec model: cbow or skip-gram
	parser.add_argument('--training_algorithm', dest='algo', type=str, default='skip-gram') 
	# optimization technique: negative-sampling or hierarchical softmax
	parser.add_argument('--optimization_technique', dest='opt', type=str, default='negative-sampling')
	# number of threads: 1-32	
	parser.add_argument('--nthreads', dest= 'nthreads', type=int, default=16)	
	args = parser.parse_args()		
	logger.info("running %s", args)
	
	# variables to fix
	num_features = 256 # dimensionality of feature vectors
	num_negative_samples = 5 # number of noise words to draw for negative sampling (5-20)
	min_word_frequency = 5 # ignore all words with total frequency lower than this
	cbow_config = 'mean' # sum/mean of context word vectors
		
	algo_bool = 1 if args.algo == 'skip-gram' else 0
	opt_bool = 1 if args.opt == 'negative-sampling' else 0	
	
	logger.info("--------------------Training--------------------")
	model = Word2Vec(Text8Corpus(args.input, 10), size=num_features, min_count=min_word_frequency, workers=args.nthreads, sg=algo_bool, hs=opt_bool, negative=num_negative_samples)
	
	# model = Word2Vec(BrownCorpus("/home/ubuntu/nltk_data/corpora/brown"), size=256, min_count=5, workers=4, sg=0, hs=0, cbow_mean=1, negative=5)
	# model = Word2Vec(LineSentence(args.input), size=200, min_count=5, workers=4)
	
	if args.output:
		logger.info("--------------------Output Model--------------------")
		model.save(args.output + '.model')
		
	if args.question:
		logger.info("--------------------Validation--------------------")
		model.accuracy(args.question)
		
	logger.info("finished running %s", program)

import gensim
print gensim.__version__
print gensim.models.word2vec.FAST_VERSION
	