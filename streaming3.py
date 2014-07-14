from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from json import loads
from sys import argv
import datetime
import os, errno
import time

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="SikqyZdm7zTQ2BwVujWqvHQNt"
consumer_secret="PFzKTkeD8OcyIxEsXR8vX7UGPXwg8Y0w3y33BZXbls9AmHNaFx"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="2556855996-0hqPxqN0BOe2Qv8VBEJ7lIHo2KZeO7TDtceLonD"
access_token_secret="VyecktLuynfc4mYQLaPuma0RDxV2hRiLotMB3ICtC1pdY"

tweets = []
tweet_times = []
counter = 0
totalcounter = 0
instances = 600

def epochToString(created_at):
    epochString = int(time.mktime(time.strptime(created_at,"%a %b %d %H:%M:%S +0000 %Y")))
    # print 'Epoch Time is .......................', epochString
    return epochString

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """



    def on_data(self, data):
        js = loads(data.decode('utf-8'))
        if 'text' in js and 'created_at' in js:
            print js['text']
            print js['created_at']
            global tweets
            global tweet_times
            global counter
            global totalcounter

            if (len(argv)>=instances and argv[3]=='short'):
                tweets.append(js['text'].replace('\n',''))
            else:tweets.append(data[:-1]+',')

            # print 'Tweets are *********************', js
            counter+=1
            if counter>=instances:
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
            return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    mkdir_p('100/'+argv[2])
    stream = Stream(auth, l)
    stream.filter(track=[argv[1]])#,languages=['en'])