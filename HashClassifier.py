import csv
import math
from collections import Counter
import string
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import re
from sets import Set

#empty dictionary to fill with tweet words in comment with ANEW words
anew = {}
keyWords = anew.keys()
lmtzr = WordNetLemmatizer()

def scoreWord(word):
	"""count a singular word's:

	V.Mean.Sum -- Valence/Pleasure Mean Sum
	A.Mean.Sum -- Arousal Mean Sum
	
	and return a coordinate tuple in the following order of (Valence, Arousal)
	"""


	global anew

	#gives stem of word/ lemmatized
	stWord = lmtzr.lemmatize(word)
	# print 'the word is', word, 'all other versions are', stWord

	if word in anew:
		# print word
		valenceMeanSum = float(anew[word]['V.Mean.Sum'])
		arousalMeanSum = float(anew[word]['A.Mean.Sum'])
		return (valenceMeanSum, arousalMeanSum,word)
	elif stWord in anew:
		valenceMeanSum = float(anew[stWord]['V.Mean.Sum'])
		arousalMeanSum = float(anew[stWord]['A.Mean.Sum'])
		return (valenceMeanSum, arousalMeanSum,stWord)

	# elif stWord + ed in anew:
	# 	valenceMeanSum = float(anew[stWord]['V.Mean.Sum'])
	# 	arousalMeanSum = float(anew[stWord]['A.Mean.Sum'])
	# 	return (valenceMeanSum, arousalMeanSum)

	else: return False

def scoreEmo(score): 
	print score
	print scoreAngle(score)
	print round((scoreAngle(score))*6)
	return (score[2],_emotions[round(scoreAngle(score)*6)%12])

def tweetCat(tweets):
	tweets = [tweet.translate(None, string.punctuation).split() for tweet in tweets]
	# print tweets
	allemotions = []
	for tweet in tweets:
		# print tweet
		emotions = map(scoreEmo,filter(None,map(scoreWord,tweet)))
		allemotions.append(emotions)
		yield  emotions

def extract_hash_tags(s):

	hashed = set(part[1:] for part in s.split() if part.startswith('#'))
	finalKeys = set()
	# return type(hashed)

	# for alice in book:
	# 	if any(anewWord in alice for anewWord in keywords):
	# 		print scoreWord(alice.lower())


	print "Your set is", hashed
	for keyword in anew:
		for word in hashed:
			# print word
			if keyword in word:
				finalKeys.add(scoreWord(keyword.lower()))
				# print scoreWord(keyword.lower())
		# if any(anewWord in word for anewWord in keyWords):
		# 	print scoreWord(word.lower())
			else:
				results =  tweetCat(tweet)
	return finalKeys


#open ANEW csv file and read in a dictionary of like word's key-values pairs
with open('ANEWwordbank.csv', 'rb') as f:
	reader = csv.DictReader(f)
	for row in reader: anew.update({row['Word']:row})

with open('aliceinwonderland.txt', 'r') as g:
	book = g.read().translate(None, string.punctuation).split()
	g.close()

tweet = "I LOVE EVERYBODY www.IamLegent/#love #everyone #gains #iloveeveryone #touchy #abandon"
print extract_hash_tags(tweet)

# keyWords = anew.keys()
# for alice in book:
# 	if any(anewWord in alice for anewWord in keyWords):
# 		# print "****"
# 		# print alice
# 		print scoreWord(alice.lower())


