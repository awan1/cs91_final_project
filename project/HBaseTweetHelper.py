__author__ = 'thegaber777'
import happybase

class HBaseTweetHelper:
    def __init__(self):
        connection = happybase.Connection('localhost')
        tables = connection.tables()
        if "tweet_table" not in tables:
            connection.create_table('tweet_table',{'tweet_info':dict()})
        self.table = connection.table('tweet_table')
        print "Connected to HBase"

    def saveTweet(self, tweetDic):
        rowId = str(tweetDic['id'])
        del tweetDic['id']
        saveDic = self.appendPrefixToDicKeys(tweetDic, "tweet_info")
        self.table.put(rowId, saveDic)
        print "SAVED TWEET: " + str(rowId)

    def iter(self):
        return self.table.scan()

    def getRetweets(self):
        for tweet_id, tweet_dict in self.iter():
            if int(tweet_dict['tweet_info:retweet_count']) > 0:
                yield (tweet_id, tweet_dict)

    def getReplies(self):
        for tweet_id, tweet_dict in self.iter():
            if tweet_dict['tweet_info:in_reply_to_user_id'] != "None":
                id = tweet_dict['tweet_info:in_reply_to_status_id']
                result = self.table.row(id)
                if len(result.keys()) > 0:
                    print "ID: " + str(id) + " RESULT: " + str(result)
                    yield (tweet_id, tweet_dict)


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
