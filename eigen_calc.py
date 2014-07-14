#!/usr/bin/python
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
from json import loads
from nltk.corpus import stopwords


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
tweets = []
mainDic = {}
stop = stopwords.words('english')
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        global tweets
        global mainDic
        global stop
        js = loads(data.decode('utf-8'))
        kamehameha = unicodedata.normalize('NFKD', js['text']).encode('ascii','ignore').lower()
        #| strips string of URLs
        super_kamehameha = re.sub(r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', "", kamehameha)
        # print super_kamehameha
        #| exclude any retweets
        # if "RT" not in super_kamehameha.upper().split(' '):            
        spirit_bomb = super_kamehameha.translate(None, string.punctuation).split()
        super_spirit_bomb = [i for i in spirit_bomb if i not in stop and len(i) > 3]
        print super_spirit_bomb
        
        tweets.append(" ".join(super_spirit_bomb))
    # tweetsMcGee(mainDic, tweets)
        print '**********************************************************', len(tweets)
        if len(tweets) >= 1000:
            f = open("tweetsMcGee.txt", 'a')
            f.write(str(tweets)
            tweets = []

        instances = 1000
        if len(tweets)>=instances:
                epochHours = str(epochToString(js['created_at'])/3600)
                epochSeconds = str(epochToString(js['created_at']))
                with open('100/'+argv[2]+'/'+epochHours+' - '+epochSeconds+' ('+str(instances)+')','a') as f:
                    if(len(argv)>3):f.write('\n'.join(tweets).encode('UTF-8'))

                    else:
                        stringy = ''
                        for tweet in tweets:
                            stringy+= tweet
                        f.write( stringy[:-1] )
                        #f.write(''.join(tweets[:-1]).encode('UTF-8'))
                        #f.write(']')
                    f.close()
                    counter = 0
                    del tweets[:]


        # xavier = []
        # for bombs in spirit_bomb:
        #     if bombs.lower() not in stop and len(bombs) > 2:
        #         xavier.append(bombs)
        # # tweets.append(xavier)
            
        #     tweets.append(spirit_bomb)
        #     xavier = [i for i in tweets if i not in stop]
        #     print xavier
        #     # print '*******************************************', spirit_bomb

        # tweetsMcGee(mainDic, tweets)

def addLinks(mainDic, key, tweet):
    for thing in tweet:
        if thing != key:
            mainDic[key][thing] += 1
    return mainDic
 
 
def tweetsMcGee(mainDic, tweets):
    for each in tweets:
        for stringy in each:
            if stringy not in mainDic:
                #mainDic[stringy] = DataPoint(stringy)
                mainDic[stringy] = Counter()
            mainDic = addLinks(mainDic, stringy, each)
 
    print '********************************************************************************************', mainDic




l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)




stream = Stream(auth, l)
stream.filter(track=[
    'World Cup'
    ])








#|  empty dictionary to fill with tweet words in comment with ANEW words  
#anew = {}

#|  open ANEW csv file and read in a dictionary of like word's key-values pairs  
#with open('ANEWwordbank.csv', 'rb') as f:
   # reader = csv.DictReader(f)
   # for row in reader: anew.update({row['Word']:row})

