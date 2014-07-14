from collections import Counter
from nltk.corpus import stopwords
from json import loads, dump
from unicodedata import normalize
import re, string


stop = stopwords.words('english')
tweets = []
sample = ['This is one tweet', 'This is a second, more lengthy tweet']
with open('/home/tsl/public_html/moods/100/steven_test/390048 - 1404176135 (600)', 'r') as infile:
	data = infile.read()
	jss = loads('['+ data.decode('utf-8').replace('\n', '') + ']')
	for js in jss:
		tweet = normalize('NFKD', js['text']).encode('ascii','ignore').lower()
		#| strips string of URLs
		tweet = re.sub(r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', "", tweet)
		# print super_kamehameha
		#| exclude any retweets
		# if "RT" not in super_kamehameha.upper().split(' '):            
		tweet = tweet.translate(None, string.punctuation).split()
		tweet = [i for i in tweet if i not in stop and len(i) > 3]
		tweets.append(tweet)

# Stevens stuff takes in 'sample' variable, give me this thing:
# tweets = [['one', 'tweet'], ['second', 'more', 'tweet']]

# Main data structure
class DataPoint:
	def __init__(self, n):
		self.name = n
		self.links = Counter()
		self.connects = 0

	def __str__(self):
		return self.name + ' obj'

	def addLink(self, link):
		self.links[link] += 1
		self.connects += 1
	def getLinks(self):
		return self.links

def addLinks(mainDic, key, tweet):
	for thing in tweet:
		if thing != key:
			mainDic[key][thing] += 1
	return mainDic


def sortw(w1, w2):
	if w1<w2: return w1,w2
	return w2,w1

mainDic = {}

most = Counter()
most_links = Counter()
for tweet in tweets:
	for w in tweet:
		most[w]+=1

topmost = dict(most.most_common(50))		

for tweet in tweets:
	for  w in tweet:
		if w in topmost:
			for w2 in tweet:
				if w2 in topmost and w2!=w:
					wa,wb = sortw(w,w2)
					most_links[wa+'|'+wb]+=1
			# if w in most2:
			# 	for w2 in tweet:
			# 		most2[w][w2]+=1

# for each in tweets:
# 	for stringy in each:
# 		if stringy not in mainDic:
# 			#mainDic[stringy] = DataPoint(stringy)
# 			mainDic[stringy] = Counter()
# 		mainDic = addLinks(mainDic, stringy, each)

#print topmost.items()
nodesj = [{'name':name, 'size':size} for name,size in topmost.items()]
#print nodesj

nodesMap = {}
for key,node in enumerate(nodesj):
	#print key
	#print node
	nodesMap.update({node['name']: key})

def stupid(key,value):
	words = key.split('|')
	return {'source':nodesMap[words[0]],'target':nodesMap[words[1]],'value':value}

# print nodesMap
# print most_links
linksj = [stupid(key,value) for key,value in most_links.items()]
# print linksj




with open('text.json', 'w') as outfile:
	dump({'nodes':nodesj, 'links':linksj}, outfile, indent=4)