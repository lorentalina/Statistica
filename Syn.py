from nltk.corpus import wordnet


def Synonyms (word):
    synonyms = []

    for syn in wordnet.synsets (word):
        for l in syn.lemmas ():
            synonyms.append (l.name().replace("_", " "))

    return (set(synonyms))

synsets = wordnet.synsets

def synonymize(text):
    for word in text:
        if word != None:
            print(synsets(word))
        else:
            print (None)
    return
            
def intersectionCmp(x,y):
        if x==None or y==None:
            return False
        #first = None
        if isinstance (x,str) and isinstance (y,str):
            x = wordnet.synsets (x)
            print (x) 
            y = wordnet.synsets (y)
            print (y)
        if isinstance(x,set) and isinstance(y,set):
            z=x
            x=y
            y=z
        else:x=set(x)        
        return bool(x.intersection(y))
