from nltk.corpus import wordnet


def Synonyms (word):
    synonyms = []

    for syn in wordnet.synsets (word):
        for l in syn.lemmas ():
            synonyms.append (l.name().replace("_", " "))

    return (set(synonyms))
