__author__ = 'thegaber777'
import happybase

class HBaseTweetHelper:
    def __init__(self):
        connection = happybase.Connection('sesame')
        self.connection = connection
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

    def filterForConnectedTweets(self, limit):
        tables = self.connection.tables()
        if "tweet_table2" in tables:
            self.connection.delete_table('tweet_table2', disable=True)
        self.connection.create_table('tweet_table2', {'tweet_info':dict()})
        table2 = self.connection.table('tweet_table2')
        counter = 0
        tweet_counter = 0
        for id, tweet in self.iter():
            counter += 1
            if counter % 100000 == 0:
                print str(counter) + " tweets processed, " + str(tweet_counter) + " tweets filtered"
            if tweet['tweet_info:in_reply_to_user_id'] != "None":
                if len(self.table.row(tweet['tweet_info:in_reply_to_status_id']).keys()) > 0:
                    table2.put(id, tweet)
                    table2.put(tweet['tweet_info:in_reply_to_status_id'], self.table.row(tweet['tweet_info:in_reply_to_status_id']))
                    tweet_counter += 1
        print "FILTER COMPLETE!"



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
