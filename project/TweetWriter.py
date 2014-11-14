__author__ = 'thegaber777'
import happybase

class TweetWriter:
    def __init__(self):
        self.connection = happybase.Connection('localhost')

    def saveTweet(self, tweetDic):
        saveDic = self.appendPrefixToDicKeys(tweetDic, "tweet_info")
        rowId = saveDic["tweet_info:"]
        self.connection.put()


    def appendPrefixToDicKeys(self, dic, prefix):
        newDic = {}
        for key in dic.keys():
            newDic[prefix + ":" + key] = dic[key]
        return newDic