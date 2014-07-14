from nltk.data import load
import re
import csv
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt


anew = {}
#open ANEW csv file and read in a dictionary of like word's key-values pairs
with open('ANEWwordbank.csv', 'rb') as f:
	reader = csv.DictReader(f)
	for row in reader: anew.update({row['Word']:row})


# def tokenize(text):
# 	return re.compile('\\W*').split(text.lower())

def wordCounter():
	wordsFreq = defaultdict(int)
	while True:
	    word = raw_input()
	    if not word:
	        break
	    wordsFreq[word] += 1

def word_count(text):
	words = re.compile('\\W*').split(text.lower())
	word_freq = dict([(word, words.count(word)) for word in set(words)])
	return word_freq

# text = "How does this word count work? Maybe this thing isn't going to"

# for word, count in wc.items():
# 	print word, "\t \t", count

def top_words(text, n=5):
	wordfreq = word_count(text)
	topwords = sorted(wordfreq.iteritems(), key = itemgetter(1), reverse=True)[:n]
	return topwords

# texts = open('aliceinwonderland.txt', 'r').read()
# topwords = top_words(texts, n=50)

# for word, count in topwords:
# 	print "%s \t %d " %(word,count)

"""Work on plotting/annotating each found frequency"""
# def plot_freq_tag(text):
	# tfw = top_words(text, n = 10)
	# words = [tfw[i][0] for i in range(len(tfw))]
	# x = range(len(tfw))
	# np = len(tfw)
	# y = []
	# for item in range(np):
	# 	y = y + [tfw[item][1]]
	# fig = plt.figure()
	# ax = fig.add_subplot(111, xlabel="Word Rank",ylabel="Word Frequency")
	# ax.set_title('Top 10 words')
	# ax.plot(x, y, 'go-', ls='dotted')
	# plt.xticks(range(0, len(words) + 1, 1))
	# plt.yticks(range(0, max(y) + 1, 10))
	# print words
	# for i, label in enumerate(words):
	# 	ax.annotate(label, (x[i], y[i]))


	# words = tokenize(text)
	# for word in words:
	# 	if word in anew:	
	# 		tfw = top_words(text, n=5)
	# 		x = range(len(tfw))
	# 		np = len(tfw)
	# 		y = []
	# 		for item in range(np):
	# 			y = y + [tfw[item][1]]
	# 		plt.axhspan(0, np, facecolor='0.5', alpha=0.5)
	# 		plt.plot(x,y,'bo',ls='dotted')
	# 		plt.xticks(range(0, 10, 1))
	# 		plt.yticks(range(0, max(y) + 1, 10))
	# 		plt.xlabel("Word Ranking")
	# 		plt.ylabel("Word Frequency")
	# 		plt.show()


text = "Either the well was very deep, or she fell very slowly, for she had \
plenty of time as she went down to look about her and to wonder what was \
going to happen next. First, she tried to look down and make out what \
she was coming to, but it was too dark to see anything; then she \
looked at the sides of the well, and noticed that they were filled with \
cupboards and book-shelves; here and there she saw maps and pictures \
hung upon pegs. She took down a jar from one of the shelves as \
she passed; it was labelled 'ORANGE MARMALADE', but to her great \
disappointment it was empty: she did not like to drop the jar for fear \
of killing somebody, so managed to put it into one of the cupboards as \
she fell past it."

print top_words(text)

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

# print stop_filter(text)
# newText = "".join(stop_filter(text))
# plot_freq_tag(newText)
# print top_words(newText)