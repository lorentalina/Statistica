#!/usr/bin/python3

import re

import xml.etree.ElementTree as ET

getprx = re.compile("{.*}")
def getPrefix(tag):
        mtc = getprx.match(tag)
        return tag[mtc.start():mtc.end()]

stripprx = re.compile("[^}]*$")
def stripPrefix(tag):
        mtc = stripprx.search(tag)
        return tag[mtc.start():mtc.end()]

def eat(iter, steps):
    for i in iter:
        if steps==0:
            return i
        steps -= 1
    raise Exception("Finished iter, some steps left.")

def parseXml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    pref = getPrefix(root.tag)
    for metadata in root.iter(pref + "metadata"):
        subpref = getPrefix(metadata[0].tag)
        for title in metadata.iter(subpref+"article-title"):
            title = title.text
            break
        date = "0000-00-00"
        for i in metadata.iter(subpref+"pub-date"):
            datedict = {}
            for j in i:
                datedict[stripPrefix(j.tag)] = j.text
            if "year" in datedict and "month" in datedict and "day" in datedict:
                date = "%s-%s-%s" % (datedict["year"], datedict["month"].rjust(2,"0"), datedict["day"].rjust(2,"0"))
        article = metadata.find(subpref + "article")
        body = article.find(subpref + "body")
        text = " ".join(body.itertext())
        yield (date, title, text)

def parseXmlGetKeys(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    pref = getPrefix(root.tag)
    for metadata in root.iter(pref + "metadata"):
        subpref = getPrefix(metadata[0].tag)
        for title in metadata.iter(subpref+"article-title"):
            title = title.text
            break
        date = "0000-00-00"
        for i in metadata.iter(subpref+"pub-date"):
            datedict = {}
            for j in i:
                datedict[stripPrefix(j.tag)] = j.text
            if "year" in datedict and "month" in datedict and "day" in datedict:
                date = "%s-%s-%s" % (datedict["year"], datedict["month"].rjust(2,"0"), datedict["day"].rjust(2,"0"))
        yield (date, title)

def parseXmlGetText(filename, steps):
    tree = ET.parse(filename)
    root = tree.getroot()
    pref = getPrefix(root.tag)
    metadata = eat(root.iter(pref + "metadata"), steps)
    subpref = getPrefix(metadata[0].tag)
    article = metadata.find(subpref + "article")
    body = article.find(subpref + "body")
    text = " ".join(body.itertext())
    return text

if __name__ == "__main__":
  for i in parseXml("records00000.xml"):
    print(i[0] + " " + i[1])