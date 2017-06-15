#!/usr/bin/python3

import itertools

from masterdemo import stem, prepText

def spanCombinations(arr, span, count):
  """ Span is like [a, b) 

Doctest

>>> sorted(list(spanCombinations(list(range(7)),5,4)))
[[0, 1, 2, 3], [0, 1, 2, 4], [0, 1, 3, 4], [0, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5], [2, 3, 4, 6], [2, 3, 5, 6], [2, 4, 5, 6], [3, 4, 5, 6]]
>>> sorted(list(spanCombinations(list(range(7)),5,2)))
[[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [2, 6], [3, 4], [3, 5], [3, 6], [4, 5], [4, 6], [5, 6]]
>>> sorted(list(spanCombinations(list(range(7)),5,1)))
[0, 1, 2, 3, 4, 5, 6]
>>> sorted(list(spanCombinations(list(range(7)),5,0)))
[]
>>> sorted(list(spanCombinations(list(range(7)),5,-1)))
[]

"""
  if count < 1:
    pass
  elif count == 1:
    for r in arr:
        yield r
  else:
    for i in range(count, span+1): # actual span
        for left in range(0,len(arr)-i+1):
            for elem in (itertools.combinations(arr[left+1:left+i-1],count-2) if count != 2 else [[]]):
                yield [arr[left]]+list(elem)+[arr[left+i-1]]


class limitDictOfSets(dict):
    """ https://stackoverflow.com/questions/2060972/subclassing-python-dictionary-to-override-setitem """
    def __init__(self, limit):
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
    def isStop(self, key):
        return True if key in super(limitDictOfSets,self).keys() and super(limitDictOfSets,self).__getitem__(key)!=False else False
    
skipgramCount = 3
skipgramSpan = 7

DB = limitDictOfSets(10)

def pushTextToDB(DB, text):
    """Text already filtered for stopwords"""
    x = [(stem(text[i]),i) for i in range(len(text)) if text[i] != None]
    for i in spanCombinations(x, skipgramSpan, skipgramCount):
        DB[tuple(k[0] for k in i)] = (i[0][1],i[-1][1])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
