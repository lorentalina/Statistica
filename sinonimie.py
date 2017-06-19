#!/usr/bin/python3

from nltk.corpus import wordnet


def Synonyms (word):
    synonyms = []

    for syn in wordnet.synsets (word):
        for l in syn.lemmas ():
            synonyms.append (l.name().replace("_", " "))

    return (set(synonyms))

synsets = wordnet.synsets

def synonymize(text):
    """ Returneaza un array care, pentru fiecare element din tokenList, are None daca acel element e None, altfel are wordnet.synsets(acelElement) 

Doctest

>>> synonymize(["Bananas",None,"very","good","."])
[[Synset('banana.n.01'), Synset('banana.n.02')], None, [Synset('very.s.01'), Synset('identical.s.02'), Synset('very.r.01'), Synset('very.r.02')], [Synset('good.n.01'), Synset('good.n.02'), Synset('good.n.03'), Synset('commodity.n.01'), Synset('good.a.01'), Synset('full.s.06'), Synset('good.a.03'), Synset('estimable.s.02'), Synset('beneficial.s.01'), Synset('good.s.06'), Synset('good.s.07'), Synset('adept.s.01'), Synset('good.s.09'), Synset('dear.s.02'), Synset('dependable.s.04'), Synset('good.s.12'), Synset('good.s.13'), Synset('effective.s.04'), Synset('good.s.15'), Synset('good.s.16'), Synset('good.s.17'), Synset('good.s.18'), Synset('good.s.19'), Synset('good.s.20'), Synset('good.s.21'), Synset('well.r.01'), Synset('thoroughly.r.02')], []]

"""
    return [synsets(i) if i != None else None for i in text]

def intersectionCmp(x,y):
    """ Daca x sau y e None, returneaza False.
Altfel, daca x sau y e un string, il converteste in set(wordnet.synsets(x)) respectiv set(wordnet.synsets(y))
Si returneaza True daca intersectia celor doua elemente nu e vida:   x.intersection(y) #x si y trebuie sa fie seturi
Iar daca ambele sunt stringuri, le compara si stem(x) == stem(y), si cu synseturi
Poti verifica daca e string cu isinstance(x,str) si isinstance(y,str)

>>> intersectionCmp(None, None)
False
>>> intersectionCmp(None, "foo")
False
>>> intersectionCmp("bar", None)
False
>>> intersectionCmp("walking", "run")
False
>>> intersectionCmp("xyzzY", "XyzzYs")
True
>>> abc = wordnet.synsets("bear"); intersectionCmp(abc, "yield")
True
>>> abc = wordnet.synsets("yield"); intersectionCmp("bears", abc)
True
>>> abc1 = wordnet.synsets("yield"); abc2 = wordnet.synsets("bears"); intersectionCmp(abc1, abc2)
True

"""
    if x == None or y == None:
        return False
    first = None
    if isinstance(x,str):
        x = wordnet.synsets(x)
    if isinstance(y,str):
        y = wordnet.synsets(y)
    if isinstance(x,set):
        pass
    elif isinstance(y, set):
        z = x
        x = y
        y = z
    else:
        x = set(x)
    return bool(x.intersection(y))
