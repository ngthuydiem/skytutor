# Example: ./word2vec.py ~/workspace/word2vec/text8 ~/workspace/word2vec/questions-words.txt ./text8
import logging
import sys
import os
import argparse
from numpy import seterr
from gensim import utils
from gensim.models.word2vec import Word2Vec

logger = logging.getLogger(__name__)
if __name__ == "__main__":
	logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
	program = os.path.basename(__file__)
			
	parser = argparse.ArgumentParser(description='Validation parameters')
	parser.add_argument('--model_file', dest='model', type=str, required=True)
	parser.add_argument('--model_type', dest='model_type', type=str, default='gensim')
	parser.add_argument('--question_file', dest='question', type=str, default='questions-words.txt')
	args = parser.parse_args()		
	logger.info("running %s", args)
				
	logger.info("--------------------Load Model--------------------")
	if args.model_type == 'C-bin':		
		model = Word2Vec.load_word2vec_format(args.model, binary=True) # C binary format
	elif args.model_type == 'C-text':	
		model = Word2Vec.load_word2vec_format(args.model, binary=False) # C text format
	else: # Gensim format
		model = Word2Vec.load(args.model)
		
	if args.question:
		logger.info("--------------------Validation--------------------")
		model.accuracy(args.question)
		
	logger.info("finished running %s", program)
