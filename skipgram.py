#!/usr/bin/python3

import itertools

from utils import *

def spanCombinations(arr, innerLimits, span = 7, count = 2):
  """ Span is like [a, b) 

Doctest

>>> q = list(range(6,-1,-1)); sorted(    [[q[x] for x in i] for i in spanCombinations(q,[0,len(q)],5,4)]    )
[[3, 2, 1, 0], [4, 2, 1, 0], [4, 3, 1, 0], [4, 3, 2, 0], [4, 3, 2, 1], [5, 3, 2, 1], [5, 4, 2, 1], [5, 4, 3, 1], [5, 4, 3, 2], [6, 4, 3, 2], [6, 5, 3, 2], [6, 5, 4, 2], [6, 5, 4, 3]]
>>> q = list(range(7)); sorted(    [[q[x] for x in i] for i in spanCombinations(q,[0,len(q)],5,2)]    )
[[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [2, 6], [3, 4], [3, 5], [3, 6], [4, 5], [4, 6], [5, 6]]
>>> q = list(range(7)); sorted(    [[q[x] for x in i] for i in spanCombinations(q,[0,len(q)],5,1)]    )
[[0], [1], [2], [3], [4], [5], [6]]
>>> q = list(range(7)); sorted(    [[q[x] for x in i] for i in spanCombinations(q,[0,len(q)],5,0)]    )
[]
>>> q = list(range(7)); sorted(    [[q[x] for x in i] for i in spanCombinations(q,[0,len(q)],5,-1)]    )
[]

"""
  if count < 1:
    pass
  elif count == 1:
    for r in range(innerLimits[0], innerLimits[1]):
      if arr[r]!=None:
        yield [r]
  else:
    for i in range(count, span+1): # actual span
        for left in range(innerLimits[0],innerLimits[1]-i+1):
            right = left+i-1
            if arr[left]== None or arr[right]==None:
                continue
            for elem in (itertools.combinations(range(left+1,right),count-2)  if count != 2 else [[]]):
              if None not in (arr[w] for w in elem):
                yield [left]+list(elem)+[left+i-1]


class limitDictOfSets(dict):
    """ https://stackoverflow.com/questions/2060972/subclassing-python-dictionary-to-override-setitem 

Doctest

>>> t = "The quick and fox fox fox fox fox fox fox fox fox jumps over the lazy dog."; t = Text(t); q = limitDictOfSets(); _ = {q.__setitem__(tuple(t[p][2] for p in i), (i[0],i[-1])) for i in spanCombinations(t.stemmed, [0,len(t)])};print(q);print(q.buildMargins());

"""
    def __init__(self, limit=10):
        #self.dict = {}
        self.limit=limit
    def __setitem__(self, key, value):
        if key not in super(limitDictOfSets,self).keys():
            super(limitDictOfSets,self).__setitem__(key,set())
        q = super(limitDictOfSets,self).__getitem__(key)
        if q!=False and value not in q:
            if self.limit == len(q):
                super(limitDictOfSets,self).__setitem__(key, False)
            else:
                q.add(value)
    def __getitem__(self, key):
        r = super(limitDictOfSets,self).__getitem__(key)
        return r if r!=False else set()
    def isStop(self, key):
        return False if key in super(limitDictOfSets,self).keys() and super(limitDictOfSets,self).__getitem__(key)!=False else True

    def buildMargins(self, limit=10):
        head = limitDictOfSets(limit)
        tail = limitDictOfSets(limit)
        head.buildMargins = tail.buildMargins = None
        for i in super(limitDictOfSets,self).keys():
            if not self.isStop(i):
                head[i[0]] = i
                tail[i[-1]] = i
        return (head, tail)
    
skipgramCount = 2
skipgramSpan = 7

DB = limitDictOfSets()




if __name__ == "__main__":
    import doctest
    doctest.testmod()
