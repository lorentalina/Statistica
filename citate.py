#!/usr/bin/python3

# Modul identificare citate

#functie care verifica daca un cuvant este un verb ce introduce citate
def isQuoteVerb( word ):	
	if (word=="says" or word=="said" or word=="writes" or word=="wrote" or word.find("argue")!=-1 or word.find("conclude")!=-1 or word.find("affirm")!=-1 
			or word.find("state")!=-1 or word.find("argue")!=-1 or word.find("confirm")!=-1 or word.find("declare")!=-1 or word.find("explain")!=-1 or word.find("remark")!=-1
			or word.find("note")!=-1 or word.find("observe")!=-1 or word.find("prove")!=-1 or word.find("show")!=-1 or word.find("emphasize")!=-1 or word.find("suggest")!=-1):
		return True
	else: 
		return False

def citationBoundaries(text):
    """Doctest

>>> print(citationBoundaries(['Simon', 'argued', ':', "''", 'The', 'quick', 'brown', 'fox', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '.', "''", "''", 'The', 'fox', 'is', 'brown', "''", ',', 'Simon', 'said']))
[[3, 16], [17, 22]]

"""
    text_length=len(text)
    quotes = []
    #salvez pozitiile la care se gasesc ghilimelele
    indexes = [i for i,x in enumerate(text) if x == "''" or x == '``']  
	
    #daca in text exista un nr impar de ghilimele, o sterg pe ultima
    if len(indexes)%2!=0:
    	indexes.pop()

    #iau cate doua ghilimele si verific daca marcheaza corect un citat
    it = iter(indexes)
    for x in it:
        y=next(it, None)
        #Simon says: "the fox is brown". / As Simon affirms, "the fox is brown". / In his research paper, Simon concluded that "the fox is brown".
        if text[x-1]==":"  or text[x-1]=="," or text[x-1]=="that" :
        	if isQuoteVerb( text[x-2]) :
        		quotes.append([x, y])
        if y<text_length-1: 
        	#"The fox is brown"(Simon, 2017) / "The fox is brown"[1] / "The fox is brown"(1) 
        	if (text[y+1]=="(" or text[y+1]=="["):
        		quotes.append([x, y])
        	#"The fox is brown", said Simon. / "The fox is brown", Simon said. / "The fox is brown", Simon Simonescu said.
        	if text[y+1]=="," and ((y<text_length-2 and isQuoteVerb(text[y+2])) or (y<text_length-3 and isQuoteVerb(text[y+3])) or (y<text_length-4 and isQuoteVerb(text[y+4]))):
        		quotes.append([x, y])
    return quotes		

def stripCitedPassages(text):
    """Doctest

>>> x = ["Ana","are","''","mere","''","says","Simon","."]; y = stripCitedPassages(x); x[6] == y[6]
True
>>> print(stripCitedPassages(['Simon', 'argued', ':', "''", 'The', 'quick', 'brown', 'fox', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '.', "''", "''", 'The', 'fox', 'is', 'brown', "''", ',', 'Simon', 'said']))
['Simon', 'argued', ':', None, None, None, None, None, None, None, None, None, None, None, None, None, None, ',', 'Simon', 'said']

"""
    q = citationBoundaries(text)
    if not q:
        return list(text)
    r = text[0:q[0][0]]
    for i in range(1,len(q)):
        r+=[None]*(q[i-1][1] - q[i-1][0] + 1) + text[q[i-1][1]+1:q[i][0]]
    r += text[q[-1][1]+1:]
    return r

if __name__ == "__main__":
    import doctest
    doctest.testmod()
