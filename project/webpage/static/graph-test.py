"""
@author: Adrian Wan

graph-test.py: a test for generating a graph visualization
"""
import networkx as nx
from networkx.readwrite import json_graph
import json
from itertools import permutations

def main():
  G = nx.Graph()
  # List of nodes. Nodes are tuples of (node_name, attribute_dict)
  node_list = [(i, {'rt':i*3}) for i in range(1,6)]

  # Add the nodes with their attribute
  for node_name, attribute_dict in node_list:
    G.add_node(node_name, rt=attribute_dict['rt'], text="test text")

  for pair in [x for x in permutations([tup[0] for tup in node_list], 2)]:
    G.add_edge(*pair)

  data = json_graph.node_link_data(G)
  with open("graph.json", 'w') as f:
    json.dump(data, f)


if __name__ == '__main__':
  main()