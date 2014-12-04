"""
@author: Adrian Wan

hbase-link-test.py: testing getting information from hbase
"""
import networkx as nx
from networkx.readwrite import json_graph
import json

from HBaseTweetHelper import HBaseTweetHelper

myTweetHelper = HBaseTweetHelper()

def getHbaseIterator():
  return myTweetHelper.iter()

def main():
  """
  Populate a graph using an iterator over our Hbase table.
  """
  G = nx.Graph()
  for tweet_id, tweet_dict in getHbaseIterator():
    # Parse the tweet out
    '''
    Information contained in tweet dict:
    - text
    - in_reply_to_status_id
    - entities
    - in_reply_to_screen_name
    - id_str
    - retweet_count
    - in_reply_to_user_id
    - created_at
    '''
    text = tweet_dict['text']
    in_reply_to_status_id = tweet_dict['in_reply_to_status_id']
    in_reply_to_user_id = tweet_dict['in_reply_to_user_id']
    retweet_count = tweet_dict['retweet_count'] + 1

    url = "http://www.twitter.com/{}/status/{}".format(username, tweet_id)

    # Add it to graph as a node
    G.add_node(node_name, retweet_count=retweet_count, url=url, text=text,
      username=username)

    # If it's in reply to something in the graph, add the edge.
    if in_reply_to_status_id in G:
      G.add_edge(tweet_id, in_reply_to_status_id)

  # Dump to JSON
  data = json_graph.node_link_data(G)
  with open("hbase-link.json", 'w') as f:
    json.dump(data, f)


if __name__ == '__main__':
  main()