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
        myFile = open(fileName,'a')
        #status = Status.parse(self.api, json.loads(data))
        #print >> myFile, "TEST"
        myStr = ""
        #print  data, "\n"
        myDict = json.loads(data)

        if 'entities' not in myDict:
            pass#print "ERROR -- NO ENTITIES"
        elif len(myDict['entities']['hashtags']) > 0:
            print >> myFile, data.encode("utf-8")
            print myDict['text'].encode("utf-8")
            myFile.close()



        return True
    def on_status(status):
        print "STATUS"

    def on_error(self, status):
        print status
        #myFile.close()



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
    print "CONSUMER_KEY =" + consumer_key
    print "CONSUMER_SECRET =" + consumer_secret
    print "ACCESS_TOKEN =" + access_token
    print "ACCESS_TOKEN_SECRET" + access_token_secret
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    """
    if len(sys.argv) < 2:
        fileName = "AllTweets.txt"
        stream.sample()
    elif sys.argv[1] == '1':
        fileName = "HappyEmoAll.txt"
        stream.filter(track=[':-)',':)','=)',':D'])
    elif sys.argv[1] == '2':
        fileName = "SadEmoAll.txt"
        stream.filter(track=[':-(',':(','=(',';('])

    else:
    """
    if len(sys.argv) < 3:
        print "USAGE <SEARCH_TERM> <OUTPUT_FILENAME>"
    #search = sys.argv[1]
    #serach = "#" + search
    fileName = sys.argv[2]
    search = sys.argv[1]
    stream.filter(track=[search])