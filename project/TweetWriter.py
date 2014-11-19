__author__ = 'thegaber777'
import happybase

class TweetWriter:
    def __init__(self):
        self.table = happybase.Connection('localhost').table('tweet_table')
        print "Connected to HBase"

    def saveTweet(self, tweetDic):
        rowId = str(tweetDic['id'])
        del tweetDic['id']
        saveDic = self.appendPrefixToDicKeys(tweetDic, "tweet_info")
        self.table.put(rowId, saveDic)


    def appendPrefixToDicKeys(self, dic, prefix):
        newDic = {}
        for key in dic.keys():
            prefixStr = prefix + ":" + key
            value = self.encodeIfStr(dic[key])
            newDic[prefix + ":" + key] = value
        return newDic

    def encodeIfStr(self, value):
        if isinstance(value, basestring):
            return value.encode("utf-8")
        return str(value)