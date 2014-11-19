import vincent
import random
import pandas as pd

def main():
  cat_1 = ['y1', 'y2', 'y3', 'y4']
  index_1 = range(0, 21, 1)
  multi_iter1 = {'index': index_1}
  for cat in cat_1:
    multi_iter1[cat] = [random.randint(10, 100) for x in index_1]

  bar = vincent.Bar(multi_iter1['y1'])
  bar.axis_titles(x='Index', y='Value')
  bar.to_json('vega.json')

if __name__ == '__main__':
  main()