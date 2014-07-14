import csv
import math
from collections import Counter
import string
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict

# insert tweets hur
tweets = ["i ##eat acorns and eggs for #breakfast", "hamburgers!", "hotdogs!", "i ##eat acorns and eggs for #breakfast", "i ##eat acorns and eggs for #breakfast"]

# 12 different emotion types
_emotions = {
	0: "Pleasant",
	1: "Happy",
	2: "Elated",
	3: "Excited",
	4: "Stressed",
	5: "Upset",
	6: "Unpleasant",
	7: "Sad",
	8: "Unhappy",
	9: "Relaxed",
	10: "Calm",
	11: "Content",
}

#counters for 12 emotion types

emotionCounter = Counter()
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
	print 'the word is', word, 'all other versions are', stWord
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

def scoreAngle(score):
	"""Pass in a scoreWord tuple, Returns radians of tuple"""
	#Divide by pi to get a transformatiom of (o, 2pi) -> (0, 2)
	angle = math.atan2((score[1]/9.0) -.5, (score[0]/9.0) -.5)/math.pi
	if angle < 0: angle +=2
	return angle

def scoreEmo(score): 
	print score
	print scoreAngle(score)
	print round((scoreAngle(score))*6)
	return (score[2],_emotions[round(scoreAngle(score)*6)%12])

def stop_filter(words):
	stopless = []
	stops =['i', 'me', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \
	'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she' \
	'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', \
	'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', \
	'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', \
	'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', \
	'as', 'unti;', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', \
	'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', \
	'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', \
	'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', \
	'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', \
	'don', 'should', 'now']
	for word in words.split():
		if word not in stops:
			stopless.append(word)
	return stopless

def tweetCat(tweets):
	tweets = [tweet.translate(None, string.punctuation).split() for tweet in tweets]
	# print tweets
	allemotions = []
	for tweet in tweets:
		emotionCounter.update(tweet)
		# for item in wordcount.items(): print("{}\t{}".format(*item))
		# print "******"
		# print tweet
		emotions = map(scoreEmo,filter(None,map(scoreWord,tweet)))
		allemotions.append(emotions)
		print stop_filter(emotionCounter)
		print "*************************************"
		yield emotions



#empty dictionary to fill with tweet words in comment with ANEW words
anew = {}
#open ANEW csv file and read in a dictionary of like word's key-values pairs
with open('ANEWwordbank.csv', 'rb') as f:
	reader = csv.DictReader(f)
	for row in reader: anew.update({row['Word']:row})
	
results =  tweetCat(tweets)
for r in results:
	print(r)




	# for tweet in tweets:
	# 	tweet1 = {}
	# 	#creates a list of scores of words that were found in ANEW
	# 	# print [(word,scoreWord(word)) for word in tweet]
	# 	scores = filter(None,map(scoreWord,tweet))
	# 	#number of total scores
	# 	n = len(scores)
	# 	# print 'A total of', n, 'scores.'
	# 	#Sums up overall tweet's scoreWord value and returns it as a tuple
	# 	total = map(sum,zip(*scores))	
	# 	# print 'Sum Total is', total
	# 	# returns Arithmetic Mean of total
	# 	amoTotal = map(lambda x: x/n,total)
	# 	# (1+scoreAngleRads(total))*6) is a translation to (0,12)
	# 	emotion = _emotions[scoreCat(total)]
		
	# 	emotions = map(scoreEmo,filter(None,map(scoreWord,tweet)))
	# 	print emotions
	


		# emotionCounter[emotion]+=1
		# # gives all emotions along with frequencies
		# print emotionCounter.most_common()


