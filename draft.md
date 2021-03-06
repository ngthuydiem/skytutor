EFFICIENT TRAINING OF NEW WORD EMBEDDING MODELS

# Why do you want to train a new word embedding model?
Specialized corpus
Another language: 

# How to train a new word embedding model?
Word2Vec with Tensorflow (Google Research) https://www.tensorflow.org/versions/master/tutorials/word2vec/index.html
Gensim (Radim Rehurek) https://radimrehurek.com/gensim/
Glove (Stanford)
Spacy https://spacy.io/docs/
fastText (Faceboook Research) https://research.facebook.com/blog/fasttext/

# Finding analogies
Vector addition/subtraction 
Vector multiplication

--> Different distance measure with t-SNE

# How to evaluate how good a model is?
Extrinsic measure: 

# Can you make this better?

# Examples: Harry Potter, Vietnamese, specialized corpus (medical, architecture...)

# Leveraging graphic cards
Like other machine learning training procedures that involve a large number of 
matrix operations, one can leverage one or more graphic cards to speed up the 
training process for better embedding models. For this work, I use a somewhat 
old graphic card GeForce GTX (compute capability, cores, RAM) that comes 
with my workstation (HP Envy , cores, Hz, RAM)

* Note: I've tried using an Amazon GPU instance with the card. The support of 
Tensorflow for this type of card is limited, hence not recommended.
