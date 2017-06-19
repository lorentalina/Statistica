	#!/usr/bin/python3

from skipgram import *
import pickle
from parse import *

class Indexer:
    """

>>> t = "the quick brown fox brown fox fox fox jumps over and lazy dog flock yeah"; db =   Indexer("foodb"); db[1] = t; q = db.getSkipgram(("brown","jump")); sorted(q)
[(1, (2, 8)), (1, (4, 8))]
>>> t = "fee faa the foo  nigh  shwee shwoo shwam bee boo bam tee too tam quee quoo quam whee whoo wham xyzzY  "; q = Indexer("foodb"); q["1"] = t*5; q["2"] = t[:-17]*5; q.validateText(t);
{'1': [[(0, 0), (1, 1), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)]], '2': [[(0, 0), (1, 1), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17)]]}
"""
    pickleThreshold = 0 #100
    lcsCountThreshold = 12
    lcsDensity = 0.2
    def __init__(self, pickleName, load = False, skipgramSpan=7, skipgramCount=2):
        if load:
            f = open(pickleName, "rb")
            r = pickle.load(self, f)
            f.close()
            return r
        self.pickleName = pickleName
        self.skipgramSpan = skipgramSpan
        self.skipgramCount = skipgramCount
        self.texts = LazyTexts()
        self.skipgrams = limitDictOfSets()
        self.pushed = 0
        self.wasUpdated = True
    def __setitem__(self, key, value):
        if key in self.texts.headers:
            #raise Exception("key %s already in texts" % key)
            return
        self.texts[key] = value
        t = self.texts[key]
        for i in spanCombinations(t.stemmed, [0, len(t)], self.skipgramSpan, self.skipgramCount):
            k = tuple(t.stemmed[j] for j in i)
            self.skipgrams[k] = (key, (i[0], i[-1]))
        self.wasUpdated = True
        self.pushed+=1
        if self.pickleThreshold>0 and self.pushed>=self.pickleThreshold:
            self.pushed=0
            f = open(self.pickleName, "wb")
            pickle.dump(self, f)
            f.close()
    def getSkipgram(self,key):
        if self.wasUpdated:
            self.wasUpdated = False
            self.head, self.tail = self.skipgrams.buildMargins()
        r = set()
        if key in self.skipgrams.keys():
            r.update(self.skipgrams[key])
        if key[0] in self.head.keys():
            for i in self.head[key[0]]:
                if tuplesHybridCmp(key, i):
                    r.update(self.skipgrams[i])
        if key[-1] in self.tail.keys():
            for i in self.tail[key[-1]]:
                if tuplesHybridCmp(key, i):
                    r.update(self.skipgrams[i])
        return r
    
    def validateText(self, text):
        queryT = Text(text)
        skMatches = {}
        for queryGramIndices in spanCombinations(queryT.stemmed, [0, len(queryT)], self.skipgramSpan, self.skipgramCount):
            queryGram = tuple(queryT.stemmed[k] for k in queryGramIndices)
            for dbMatch in (self.getSkipgram(queryGram)):
                if dbMatch[0] not in skMatches:
                    skMatches[dbMatch[0]] = set()
                skMatches[dbMatch[0]].add(((queryGramIndices[0], queryGramIndices[-1]),dbMatch[1]))
        r = {}        
        for dbTKey in skMatches.keys():
            dbT = self.texts[dbTKey]
            queryTOuterLimits = (0, len(queryT))
            cover = []
            for gram in sorted(skMatches[dbTKey]):
                if gram[0][0]>=queryTOuterLimits[0]:
                    lcs = LCS(dbT, gram[1], (0, len(dbT)), queryT, gram[0], queryTOuterLimits, minDensity = self.lcsDensity, cmpFunc = hybridCmp)
                    if len(lcs)>=self.lcsCountThreshold:
                        cover.append(lcs)
                        queryTOuterLimits = (lcs[-1][1]+1, len(queryT))
            if cover:
                r[dbTKey] = cover
        return r
        
class LazyTexts:
    cacheMax = 100
    def __init__(self):
        self.headers = {}
        self.cacheCount = 0
        self.cacheDict = {}
        self.lastUsed = []
    def __setitem__(self, key, value):
        if key in self.headers:
            #raise Exception("key %s already in texts" % key)
            return
        self.headers[key] = value
    def __getitem__(self, key):
        if key in self.cacheDict:
            index = self.lastUsed.index(key)
            self.lastUsed.append(self.lastUsed.pop(index))
        else:
            if self.cacheCount>=self.cacheMax:
                popKey = self.lastUsed.pop(0)
                del self.cacheDict[popKey]
            else:
                self.cacheCount += 1
            self.cacheDict[key] = Text(parseXmlGetText(*self.headers[key]))
            self.lastUsed.append(key)
        return self.cacheDict[key]
    


if __name__=="__main__":
    import doctest
    doctest.testmod()



 

