from flask import render_template
from flask import request
from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/ask')
def ask():
	return render_template("ask.html")

from gensim.models import word2vec
model = word2vec.Word2Vec.load('/home/ubuntu/skytutor/word2vec/models/enwiki-skip-gram-negative-sampling.model')
#model = word2vec.Word2Vec.load('models/300features_40minwords_10context')
#model = word2vec.Word2Vec.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True)

@app.route('/reply', methods=['POST','GET'])
def ask_gensim():
	words = request.form['words']
	wordlist = words.split()
	if wordlist:
		if len(wordlist) == 1:
			word = wordlist[0]
			try:
				similar_words = model.most_similar(word)
				result = ''
				for word, similarity in similar_words:
					if similarity >= 0.6:
						result += word + ' '				
				return '"%s" is most similar to "%s"' % (words,result)
			except:
				return 'I haven\'t learnt about "%s".' % (words)
		else:
			result = model.doesnt_match(wordlist)
			return '"%s" is most different from "%s"' % (result,words)
	else:
		return 'Please ask!'