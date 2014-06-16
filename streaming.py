from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv
import math
from collections import Counter
import string

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="SikqyZdm7zTQ2BwVujWqvHQNt"
consumer_secret="PFzKTkeD8OcyIxEsXR8vX7UGPXwg8Y0w3y33BZXbls9AmHNaFx"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="2556855996-0hqPxqN0BOe2Qv8VBEJ7lIHo2KZeO7TDtceLonD"
access_token_secret="VyecktLuynfc4mYQLaPuma0RDxV2hRiLotMB3ICtC1pdY"

emotionCounter = Counter()
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        #print data
        f = open("feels.txt", 'a')
        tweet = json.loads(data)['text']
        tweet = tweet.encode('UTF-8')


        print "\n", "\n", tweetCat([tweet])
        # #counters for 12 emotion types
        # emotionCounter[emotion] += 1
        # print 'EMOTION COUNTER TALLY CURRENTLY ATM:', emotionCounter.most_common()
        



        f.write(tweet + "\n" + "\n")
        f.close()
        return True

    def on_error(self, status):
        print status

def scoreWord(word):
    """count a singular word's:

    V.Mean.Sum -- Valence/Pleasure Mean Sum
    A.Mean.Sum -- Arousal Mean Sum
    
    and return a coordinate tuple in the following order of (Valence, Arousal)
    """
    global anew
    if word in anew:
        print word
        valenceMeanSum = float(anew[word]['V.Mean.Sum'])
        arousalMeanSum = float(anew[word]['A.Mean.Sum'])
        return (valenceMeanSum, arousalMeanSum)
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
    return [_emotions[round(scoreAngle(score)*6)%12]]           #column[1][score[0]] for column in anew, ; need to get the word assoc. with it!

def tweetCat(tweets):
    tweets = [tweet.translate(None, string.punctuation).split() for tweet in tweets]
    print tweets
    allemotions = []
    for tweet in tweets:
        emotions = map(scoreEmo,filter(None,map(scoreWord,tweet)))
        allemotions.append(emotions)
    return allemotions

    #empty dictionary to fill with tweet words in comment with ANEW words
anew = {}
#open ANEW csv file and read in a dictionary of like word's key-values pairs
with open('ANEWwordbank.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader: anew.update({row['Word']:row})
    
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

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




stream = Stream(auth, l)
stream.filter(track=[
    'spain'
    ])


# optative_mood = ['May', 'if only', 'save']
# imperative_mood = ['go', 'do','run', 'i have to', 'would', 'could']
# , 'would', 'could', 'actually', 'all in all', 'certainly', 'cleraly', 'doubtful', 'debatable', 'essentially', 'fortunately', 
# 'unfortunately', 'in fact', 'inevitably', 'likely', 'maybe if', 'without a doubt', 'positively', 'really', 'technically',
#  'without a doubt', 'undeniably'