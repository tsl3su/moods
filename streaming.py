from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv
import math
from collections import Counter
import string
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import time
import datetime

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="SikqyZdm7zTQ2BwVujWqvHQNt"
consumer_secret="PFzKTkeD8OcyIxEsXR8vX7UGPXwg8Y0w3y33BZXbls9AmHNaFx"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="2556855996-0hqPxqN0BOe2Qv8VBEJ7lIHo2KZeO7TDtceLonD"
access_token_secret="VyecktLuynfc4mYQLaPuma0RDxV2hRiLotMB3ICtC1pdY"

lmtzr = WordNetLemmatizer()
emotionCounter = Counter()
wordCounter = Counter()
emojiCounter = Counter()


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
# 9 different Emoji codes
_emojis = {
    "\xF0\x9F\x98\x83": "Happy",        # \xF0\x9F\x98\x83 - Happy [1500]
    "\xF0\x9F\x98\x8C": "Relaxed",      ## \xF0\x9F\x98\x8C - relieved face [315]
    "\xF0\x9F\x98\x84": "Elated",       ## \xF0\x9F\x98\x84 - smiling face with open mouth and smiling eyes[1500]
    "\xF0\x9F\x98\x9D": "Excited",      ## \xF0\x9F\x98\x9D - face with stuck-out toungue and tightly closing eyes [1211]
    "\xF0\x9F\x98\xB3": "Stressed",     ## \xF0\x9F\x98\xB3 - Flushed face [969]
    "\xF0\x9F\x98\xA1": "Upset",        ## \xF0\x9F\x98\xA1 - Red pouting face [670]
    "\xF0\x9F\x98\x9E": "Unhappy",      ## \xF0\x9F\x98\x9E - disappointed face [635]
    "\xF0\x9F\x98\xA2": "Sad",          ## \xF0\x9F\x98\xA2 - crying face [508]
    "\xF0\x9F\x98\x8A": "Pleasant"  # \xF0\x9F\x98\x8A - smiling face with smiling eyes [1460]
}


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        #print data
        f = open("feels.txt", 'a')
        if 'text' in json.loads(data):
            # print json.loads(data)
            tweet = json.loads(data)['text']
            tweet = tweet.encode('UTF-8')


            # print "\n", "\n",
            results = tweetCat([tweet])
            for r in results:
                print(r)
            # #counters for 12 emotion types
            # emotionCounter[emotion] += 1
            # print 'EMOTION COUNTER TALLY CURRENTLY ATM:', emotionCounter.most_common()
            



            f.write(tweet + "\n" + "\n")
            f.close()
            return True
        else: print json.loads(data) 

    def on_error(self, status):
        print status

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
    #   valenceMeanSum = float(anew[stWord]['V.Mean.Sum'])
    #   arousalMeanSum = float(anew[stWord]['A.Mean.Sum'])
    #   return (valenceMeanSum, arousalMeanSum)

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
    return _emotions[round(scoreAngle(score)*6)%12]           #column[1][score[0]] for column in anew, ; need to get the word assoc. with it!

def search(tweet):
    for key in _emojis.keys():
        # print key
        # emojis = _emojis[key]
        # yield emojis
        if key in tweet:
            # print "key: %s, value: %s" % (key, _emojis[key])
            yield _emojis[key]
            print _emojis[key]
        # else: return False

def tweetCat(tweets):
    tweets = [tweet.translate(None, string.punctuation).split() for tweet in tweets]
    # print tweets
    allemotions = []
    for tweet in tweets:
        ts = time.time()
        emojis = search(tweet)
        # print type(emojis)
        # for emoji in emojis: 
        #     emojiCounter[emoji]+=1
        #     # print 'EMOJI IS:', emoji
        print tweet
        # for word in tweet: wordCounter[word]+=1
        emotions = map(scoreEmo,filter(None,map(scoreWord,tweet)))
        print 'emotions',emotions
        allemotions.append(emotions)
        for feeling in emotions: emotionCounter[feeling]+=1
        st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')       #%Y-%m-%d 

        
        yield emotions
        #returns top 20 ten words in emotion counter
        # print 'This is the top twenty for Word Counter', wordCounter.most_common(20)

        with open('/home/tsl/public_html/randomtest3.csv', 'a') as outfile:
            # json.dump(emotionCounter, outfile)
            totalEmotion = 0
            for each in emotionCounter:
                totalEmotion += emotionCounter[each]
            for item in emotionCounter: 
                # print 'type of ITEM IS', item
                
               # print item
                #print float(emotionCounter[item])
                if item != 'Unpleasant' and item != 'Stressed' and item != 'Unhappy' and item != 'Elated':
                    outfile.write(item + ',' + str(float(emotionCounter[item])/float(totalEmotion)) + ','+ str(st) + ',' + '\n')
                    emotionCounter[item] = 0
                # Percentages of Emotions
                # print 'emotionCounter[Calm': 3197,item] is', emotionCounter[item]

            print 'Total Emotion is', totalEmotion
        print 'Emotion Counter is: ', emotionCounter

        print 'This is the Emoji Counter: ', emojiCounter.most_common()
        print "*************************************"


#empty dictionary to fill with tweet words in comment with ANEW words
anew = {}
#open ANEW csv file and read in a dictionary of like word's key-values pairs
with open('ANEWwordbank.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader: anew.update({row['Word']:row})
    
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)




stream = Stream(auth, l)
stream.filter(track=[
    'Spain'
    ])


# optative_mood = ['May', 'if only', 'save']
# imperative_mood = ['go', 'do','run', 'i have to', 'would', 'could']
# , 'would', 'could', 'actually', 'all in all', 'certainly', 'cleraly', 'doubtful', 'debatable', 'essentially', 'fortunately', 
# 'unfortunately', 'in fact', 'inevitably', 'likely', 'maybe if', 'without a doubt', 'positively', 'really', 'technically',
#  'without a doubt', 'undeniably