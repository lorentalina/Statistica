#!/usr/bin/python3 -i

import os
from indexer import *
import sys

def limitYield(iter, maxSteps):
    for i in iter:
        if maxSteps <= 0:
            break
        yield i
        maxSteps -= 1

directory = sys.argv[1]
oldCD = os.getcwd()
textDB = Indexer("foopickle")
#print(list(os.walk(directory)))
walker = ("%s/%s" % (p[0],x) for p in os.walk(directory) for x in p[2] if x[-4:]==".xml")
for q in limitYield(walker, 10): #https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    #print(q)
    nr = 0
    for t in parseXmlGetKeys(q):
        print(t)
        textDB[t] = (q,nr) 
        nr += 1

queryDB = LazyTexts()
for q in limitYield(walker, 1): #reuse to avoid pushing texts that were also pushed to textDB
    nr = 0
    for t in parseXmlGetKeys(q):
        print(t)
        queryDB[t] = (q,nr) 
        nr += 1

for i in queryDB.headers:
    print(textDB.validateText(i))

