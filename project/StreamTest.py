from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sys
from tweepy.utils import import_simplejson, urlencode_noplus
json = import_simplejson()
# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""
search = ""
fileName = ""
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        myDict = json.loads(data)

        if 'entities' not in myDict:
            return
        else:
            self.save_tweet(myDict)

        return True

    def on_status(status):
        print "STATUS"

    def on_error(self, status):
        print status

    def save_tweet(self, fullDict):
        """
        Takes in a full tweet dictionary and writes only the significant fields
        to a file
        """
        myFile = open(fileName,'a')
        tweetDict = {}

        tweetDict['text'] = fullDict['text']
        tweetDict['in_reply_to_status_id'] = fullDict['in_reply_to_status_id']
        tweetDict['id'] = fullDict['id']
        tweetDict['entities'] = fullDict['entities']
        tweetDict['in_reply_to_screen_name'] = fullDict['in_reply_to_screen_name']
        tweetDict['id_str'] = fullDict['id_str']
        tweetDict['retweet_count'] = fullDict['retweet_count']
        tweetDict['in_reply_to_user_id'] = fullDict['in_reply_to_user_id']
        tweetDict['created_at'] = fullDict['created_at']

        tweetStr = json.dumps(tweetDict).encode("utf-8")

        print >> myFile, tweetStr
        myFile.close()

def readInKeys():
    global consumer_key, consumer_secret, access_token, access_token_secret
    file = open("PRIVATE_TWITTER_KEYS", "r")
    keys = file.read().splitlines()
    consumer_key = keys[0]
    consumer_secret = keys[1]
    access_token = keys[2]
    access_token_secret = keys[3]

if __name__ == '__main__':
    readInKeys()
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    if len(sys.argv) < 2:
        print "USAGE <OUTPUT_FILENAME>"

    fileName = sys.argv[1]
    stream.sample()