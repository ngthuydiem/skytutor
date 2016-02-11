from flask import render_template
from flask import request
from flask import Markup
from app import app
from parse import *

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/ask')
def ask():
	return render_template("ask.html")

from gensim.models import word2vec
model = word2vec.Word2Vec.load('/home/ubuntu/skytutor/word2vec/models/enwik9_text-skip-gram-negative-sampling.model')
#model = word2vec.Word2Vec.load('/home/ubuntu/skytutor/word2vec/models/enwiki-skip-gram-negative-sampling.model')
#model = word2vec.Word2Vec.load('models/300features_40minwords_10context')
#model = word2vec.Word2Vec.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True)

@app.route('/reply', methods=['POST','GET'])
def ask_gensim():
	words = request.form['words']		
	
	if words.startswith("#"):
		words = words[1:]		
		result = model.doesnt_match(words.split())	
		response = '"%s" is the most unrelated out of "%s"' % (result, words)
	else:
		try:		
			pos = []
			neg = []
			for word in words.split():
				if word[0] == '-':
					neg.append(word[1:])
				else:
					pos.append(word)					
			similar_words = model.most_similar(positive=pos, negative=neg)
			result = ''
			for word, similarity in similar_words:
				if similarity >= 0.6:
					result += '%s %.2f ' %(word, similarity)
					#result += '%s ' %(word)
			if not result:
				result = str(similar_words[0])
			response = '"%s" is/are most related to "%s"' % (words,result)
		except:
			response = 'I haven\'t learnt about "%s".' % (words)			
	return "<h1>%s</h1>" % response