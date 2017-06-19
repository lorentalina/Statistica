#!/usr/bin/python3

from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import word_tokenize
from citate import stripCitedPassages
#from sinonimie import synonymize
import itertools
from LCS import LCS

from nltk.stem.porter import PorterStemmer

"""
                                                           --> skipgram stemDB / stemQuery
                                                           |
tokenizer -> stripCitedPassages -> stopper --> stemmer ------> stemCmp
   |                                       |
   --> prettyPrinter                       --> synseter -----> synsetCmp

"""


tokenizer = word_tokenize

stp = set(stopwords.words('english'))
def stopper(text):
    """ https://stackoverflow.com/questions/5486337/how-to-remove-stop-words-using-nltk-or-python """
    if isinstance(text, str):
        return text if text!= None and text not in stp else None
    return [word if word.lower() not in stp else None for word in text]

stem = PorterStemmer().stem
def stemmer(text):
    if isinstance(text, str):
        return stem(text) if text != None else None
    return [stem(i) if i != None else None for i in text]

synsets = wordnet.synsets
def synonymize(text):
    if isinstance(text, str):
        return set(synsets(text)) if text!= None else None
    return [set(synsets(i)) if i != None else None for i in text]

def nonvoidIntersection(a, b):
    if a == None or b == None:
        return False
    if len(a) > len(b):
        c = b; b = a; a = c
    for i in a:
        if i in b:
            return True
    return False

def tuplesHybridCmp(x,y):
    """

>>> tuplesHybridCmp(["xyzzY", "yield", "banana"],["XyzZy", "bears", "banana"])
True
>>> tuplesHybridCmp(["xyzzY", "yield", None],["XyzZy", "bears", None])
False
>>> tuplesHybridCmp(["xyzzY", "yield", None],["XyzZy", "bears", "banana"])
False
>>> tuplesHybridCmp(["xyzzY", "yield", "banana"],["XyzZy", "bears", "apples"])
False

"""
    if len(x)<=0:
        raise Exception("len(x) <= 0")
    if len(x)!=len(y):
        raise Exception("len(x) != len(y)")
    for i in range(len(x)):
        if not hybridCmp(x[i],y[i]):
            return False
    return True

def hybridCmp(x,y):
    """ Arguments can be either simple unstemmed strings, or Text array 

>>> hybridCmp(None, None)
False
>>> hybridCmp(None, "foo")
False
>>> hybridCmp("bar", None)
False
>>> hybridCmp("walking", "run")
False
>>> hybridCmp("xyzzY", "XyzzYs")
True
>>> abc = Text.get("bear"); hybridCmp(abc, "yield")
True
>>> abc = Text.get("yield"); hybridCmp("bears", abc)
True
>>> abc1 = Text.get("yield"); abc2 = Text.get("bears"); hybridCmp(abc1, abc2)
True

"""
    if x == None or y == None:
        return False
    if isinstance(x,str) and isinstance(y,str) and stemmer(x) == stemmer(y):
        return True
    if isinstance(x,str):
        x = Text.get(x)
    if isinstance(y,str):
        y = Text.get(y)
    if x[2] == y[2] != None:
        return True
    return nonvoidIntersection(x[3],y[3])

synseter = synonymize

class Text:
 def __len__(self):
  return self.dataLen
 def __init__ (self, text):
  if isinstance(text, str):
   text = tokenizer(text)
  self.dataLen = len(text)
  self.text = text
  self.stopped = stopper(self.text)
  self.stemmed = stemmer(self.stopped)
  self.synsets = synseter(self.stopped)

 def __getitem__(self, key):
   return [self.text[key], self.stopped[key], self.stemmed[key], self.synsets[key]]
 
 @staticmethod
 def get(token):
   stopped = stopper(token)
   stemmed = stemmer(stopped)
   synsets = synseter(stopped)
   return [token, stopped, stemmed, synsets]


if __name__=="__main__":
    import doctest
    doctest.testmod()
