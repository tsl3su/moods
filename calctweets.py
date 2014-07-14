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
from os import listdir
from os.path import isfile, join
import re
import sys
import glob
import unicodedata


#####################################################################
##  Obtain Twitter's API keys and place under Consumer and Access  ##
#####################################################################

#|  Go to http://dev.twitter.com and create an app.              
#|  The consumer key and secret will be generated for you after  
consumer_key="SikqyZdm7zTQ2BwVujWqvHQNt"
consumer_secret="PFzKTkeD8OcyIxEsXR8vX7UGPXwg8Y0w3y33BZXbls9AmHNaFx"

#|  After the step above, you will be redirected to your app's page.  
#|  Create an access token under the the "Your access token" section  
access_token="2556855996-0hqPxqN0BOe2Qv8VBEJ7lIHo2KZeO7TDtceLonD"
access_token_secret="VyecktLuynfc4mYQLaPuma0RDxV2hRiLotMB3ICtC1pdY"

lmtzr = WordNetLemmatizer()
emotionCounter = Counter()
timeEmotionCounter = Counter()
numOfEmo = 0

#| 12 different emotion types
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

def scoreWord(word):
    """count a singular word's:

    V.Mean.Sum -- Valence/Pleasure Mean Sum
    A.Mean.Sum -- Arousal Mean Sum
    
    and returns a coordinate tuple in the following order of (Valence, Arousal).

    Attributes:
        anew: references csv file of ANEW words with respective valence and arousal key-values
        stWord: using WordNetLemmatizer, returns stem and all other versions of the word

    """

    global anew
    stWord = lmtzr.lemmatize(word)

    if word in anew:
        valenceMeanSum = float(anew[word]['V.Mean.Sum'])
        arousalMeanSum = float(anew[word]['A.Mean.Sum'])
        return (valenceMeanSum, arousalMeanSum,word)
    elif stWord in anew:
        valenceMeanSum = float(anew[stWord]['V.Mean.Sum'])
        arousalMeanSum = float(anew[stWord]['A.Mean.Sum'])
        return (valenceMeanSum, arousalMeanSum,stWord)
    else: return False

def scoreAngle(score):
    """Passes in a scoreWord function's tuple, Returns radians of tuple

    """

    #|  Divide by pi to get a transformation of (o, 2pi) -> (0, 2)  
    angle = math.atan2((score[1]/9.0) -.5, (score[0]/9.0) -.5)/math.pi
    if angle < 0: angle +=2
    return angle

def scoreEmo(radians): 
    """Takes in a radians value, and classifies into a key value from the dictionary '_emotions'

    Attributes:
        scoreAngle: provides radians value
        round: rounds scoreAngle to nearest integer value

    """ 

    return _emotions[round(scoreAngle(radians)*6)%12] 

def writeOutPercent(filename, epochTime):
    """Takes in a filename and an epochTime, Creates a csv file in directory 'home/public html'
    and loops through each emotion in emotionCounter to append 'key,date,percentValue' for each
    new line in the csv file.  

    Attributes:
        numOfEmo: sum of all values in emotionCounter  
        emoPercentage: the percentage an emotion has out of numOfEmo

    """

    global numOfEmo
    with open('/home/tsl/public_html/' + filename + 'percent.csv', 'a') as outfileone:
        numOfEmo = sum(timeEmotionCounter.itervalues())
        for emotion in timeEmotionCounter:
            emoPercentage = float(timeEmotionCounter[emotion])/float(numOfEmo +1)
            outfileone.write(emotion + ',' + str(emoPercentage) + ','+ str(epochTime) + ',' + '\n')
                        
def writeOutRaw(filename, epochTime):
    """Takes in a filename and an epochTime, Creates a csv file in directory 'home/public html' and 
    loops through each emotion in emotionCounter to append 'key,date,rawValue' for each new line in 
    the csv file.  

    """

    with open('/home/tsl/public_html/' + filename + 'raw.csv', 'a') as outfiletwo:
        for item in timeEmotionCounter:
            outfiletwo.write(item + ',' + str(timeEmotionCounter[item]) + ','+ str(epochTime) + ',' + '\n')
            timeEmotionCounter[item] = 0
    print 'Emotion Counter is: ', emotionCounter
    print "*************************************"

def epoched(created_at):
    """Takes in twitter's json unicode object, 'created_at' in the form "%a %b %d %H:%M:%S +0000 %Y"
    and returns it in epochtime as an integer 

    """

    epochy = int(time.mktime(time.strptime(created_at,"%a %b %d %H:%M:%S +0000 %Y")))
    return epochy 

def tweetOneCat(tweet):
    """Passes in a tweet, scores it and stores found emotions in a list

    Attributes:
        emotions: list of emotions found in a tweet

    """
    global timeOfTweet
    global epochTime

    epochTime = epoched(timeOfTweet)
    emotions = map(scoreEmo,filter(None,map(scoreWord,tweet)))
    return emotions

def tweetCat(tweets):
    """Passes in a list of tweets, and loops through each tweet categorizing the tweet's emotions
    whilst keeping count of each emotion. After the set interval is passed, it writes out to 
    ''raw.csv and ''percent.csv for the respective values.

    Attributes:
        epochTime: time of current tweet being handled 
        firstTweetTime: instantiates the first tweet's time to be categorized, effectively giving
        a starting place of reference to start the 'timer' for the interval to be compared to.
        stringified_tweet: converts the unicodedata (from the json object that is the tweet) to
        a string.
        tweetText: ignores punctuation and splits up the text into individual words.
        
    """

    global numOfEmo
    global timeOfTweet
    firstTweetTime = epoched(tweets[0]['created_at'])

    for tweet in tweets:
        stringified_tweet = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore') #******** unicode to string
        tweetText = stringified_tweet.translate(None, string.punctuation).split()
        timeOfTweet = tweet['created_at']
        epochTime = epoched(timeOfTweet)      
        emotions = tweetOneCat(tweetText)
        print 'These are your emotions:', emotions
        for emotion in emotions: timeEmotionCounter[emotion]+=1
        if epochTime - firstTweetTime >= 4:
            writeOutRaw("GERTest", epochTime)
            writeOutPercent("GERTest", epochTime)
            firstTweetTime = epochTime

#|  empty dictionary to fill with tweet words in comment with ANEW words  
anew = {}

#|  open ANEW csv file and read in a dictionary of like word's key-values pairs  
with open('ANEWwordbank.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader: anew.update({row['Word']:row})

#|  creates a list of all files under a certain directory  
onlyfiles = [ f for f in listdir("/home/tsl/public_html/moods/100/steven_test") if isfile(join("/home/tsl/public_html/moods/100/steven_test",f)) ]

#|  Goes through all the files in the directory onlyfiles and categorizes each tweet in every file  
for fi in onlyfiles:
    with open("/home/tsl/public_html/moods/100/steven_test/" + fi) as f:
        data = ('['+f.read().decode('utf-8').replace('\n', '')+']')
        results = json.loads(data)
        calculated = tweetCat(results)