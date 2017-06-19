#!/usr/bin/python3


def floatgte(a, b):
    """ a >= b """
    if a >= b:
        return True
    elif abs(a-b)<0.1:
        return True
    return False


class offsetList(list):
    def __init___(self, initval, size, offset):
        self.offset = offset
        self.list = [initval] * size
    def __getitem__(self, key):
        return self.list[key - offset]

def mkMatrix(initVal,firstDim, secondDim, firstOffset, secondOffset): #please give immutable initVal
    """ Something like [[0]*5]*3 gives you a nasty bug. You are in for a treat.
Use this function instead."""
    r = []
    for i in range(firstDim):
        r.append([initVal]*secondDim)
    return r

def density(cnt, leftLim, rightLim):
    if leftLim==rightLim:
        return 0
    return float(cnt) / float(rightLim - leftLim)


def defaultCmpFunc(x1,x2):
    return x1==x2!=None

def LCS(array1, innerLimits1, outerLimits1,
        array2, innerLimits2, outerLimits2,
        minDensity=0.2, cmpFunc=defaultCmpFunc, maxItersNotUpdated = 15):
    """
 
>>> test1="abcabcadz";test2="acabdefghikzyv";LCSsimpleReversed(test1,[0,len(test1)],test2,[0,len(test2)],minDensity = 0,cmpFunc=defaultCmpFunc, maxItersNotUpdated = 15)
[(0, 0), (2, 1), (3, 2), (4, 3), (7, 4), (8, 11)]
>>> test1="abcabcadz";test2="acabdefghikzyv";LCSsimple(test1,[0,len(test1)],test2,[0,len(test2)],minDensity = 0,cmpFunc=defaultCmpFunc, maxItersNotUpdated = 15)
[(0, 0), (2, 1), (3, 2), (4, 3), (7, 4), (8, 11)]
>>> test1="abcabcadz";test2="acabdefghikzyv";LCSsimple(test1,[1,len(test1)],test2,[1,len(test2)],minDensity = 0,cmpFunc=defaultCmpFunc, maxItersNotUpdated = 15)
[(2, 1), (3, 2), (4, 3), (7, 4), (8, 11)]
>>> test1="abcabcadz";test2="acabdefghikzyv";LCS(test1,[3,5],[0,len(test1)],test2,[3,5],[0,len(test2)],minDensity=0.2,cmpFunc=lambda x,y:x==y, maxItersNotUpdated = 15)
[(0, 0), (2, 1), (4, 3), (8, 11)]

"""
    return  ( 
        LCSsimpleReversed(array1, [outerLimits1[0],innerLimits1[0]] , array2, [outerLimits2[0],innerLimits2[0]], minDensity, cmpFunc, maxItersNotUpdated) +
        LCSsimple(array1, innerLimits1 , array2, innerLimits2, 0, cmpFunc, maxItersNotUpdated) +
        LCSsimple(array1, [innerLimits1[1],outerLimits1[1]] , array2, [innerLimits2[1],outerLimits2[1]], minDensity, cmpFunc, maxItersNotUpdated) 
      )

def LCSsimpleReversed(array1, innerLimits1, array2, innerLimits2, minDensity, cmpFunc, maxItersNotUpdated):
    tarr1 = list(reversed(array1))
    tarr2 = list(reversed(array2))
    tinnerLimits1 = [len(array1) - innerLimits1[1], len(array1) - innerLimits1[0]]
    tinnerLimits2 = [len(array2) - innerLimits2[1], len(array2) - innerLimits2[0]]
    r = LCSsimple(tarr1, tinnerLimits1, tarr2, tinnerLimits2, minDensity, cmpFunc, maxItersNotUpdated)
    r = [(len(array1) - i[0] - 1, len(array2) - i[1] - 1) for i in reversed(r)]
    return r

def LCSsimple(array1, innerLimits1, 
        array2, innerLimits2, 
        minDensity, cmpFunc, maxItersNotUpdated):
    """limits are like: (a,b) -> [a,b) """
    
    if innerLimits1[0] < 0: raise Exception("innerLimits1[0] is %d" % innerLimits1[0])
    if innerLimits1[1] > len(array1): raise Exception("innerLimits1[1] is %d, len(array1) is %d" % innerLimits1[0] % len(array1))
    if innerLimits1[0]>innerLimits1[1]: raise Exception("innerLimits1[0] is %d, innerLimits1[1] is %d" % tuple(innerLimits1))
    if innerLimits2[0] < 0: raise Exception("innerLimits2[0] is %d" % innerLimits2[0])
    if innerLimits2[1] > len(array2): raise Exception("innerLimits2[1] is %d, len(array2) is %d" % innerLimits2[0] % len(array2))
    if innerLimits2[0]>innerLimits2[1]: raise Exception("innerLimits2[0] is %d, innerLimits2[1] is %d" % tuple(innerLimits2))

    #initial count between inner Limits
    
    maxPos = (None, None)
    maxCnt = 0
    maxDensity1 = 0
    maxDensity2 = 0
    arr=mkMatrix(0, innerLimits1[1]+1, innerLimits2[1]+1, innerLimits1[0], innerLimits2[0])                       
    prevLink = mkMatrix((None,None), innerLimits1[1]+1, innerLimits2[1]+1, innerLimits1[0], innerLimits2[0])      
    hasAdded = mkMatrix(False, innerLimits1[1]+1, innerLimits2[1]+1, innerLimits1[0], innerLimits2[0]) 
    itersNotUpdated = 0
    for abc in range(0, max(innerLimits1[1]-innerLimits1[0], innerLimits2[1]-innerLimits2[0])):
        if maxItersNotUpdated > 0 and itersNotUpdated > maxItersNotUpdated:
            break
        itersNotUpdated +=1 
        it = []
        pos1 = innerLimits1[0] + abc
        it += [(pos1,pos2) for pos2 in range(innerLimits2[0],min(innerLimits2[1],innerLimits2[0]+abc)) ] if pos1 < innerLimits1[1] else []
        pos2 = innerLimits2[0] + abc
        it += [(pos1,pos2) for pos1 in range(innerLimits1[0],min(innerLimits1[1],innerLimits1[0]+abc)) ] if pos2 < innerLimits2[1] else []
        pos1, pos2 = innerLimits1[0] + abc, innerLimits2[0] + abc
        it += [(pos1,pos2)] if pos1 < innerLimits1[1] and pos2 < innerLimits2[1] else []
         
        for pos1,pos2 in it:
            currentCnt = max(
                1 + arr[pos1][pos2] if cmpFunc(array1[pos1],array2[pos2]) #only here do not +1 the indices
                else 0,
                arr[pos1+1][pos2],
                arr[pos1][pos2+1]
            )
            
            arr[pos1+1][pos2+1] = currentCnt
            if arr[pos1+1][pos2] == currentCnt:
                
                prevLink[pos1+1][pos2+1] = (prevLink[pos1+1][pos2]
                    if not hasAdded[pos1+1][pos2]
                    else (pos1+1,pos2))
            elif arr[pos1][pos2+1] == currentCnt:
                
                prevLink[pos1+1][pos2+1] = (prevLink[pos1][pos2+1]
                    if not hasAdded[pos1][pos2+1]
                    else (pos1,pos2+1))
            else:
                
                hasAdded[pos1+1][pos2+1]=True
                prevLink[pos1+1][pos2+1] = (prevLink[pos1][pos2]
                    if not hasAdded[pos1][pos2]
                    else (pos1,pos2))

            
            currentDensity1 = density(currentCnt, innerLimits1[0], pos1)
            currentDensity2 = density(currentCnt, innerLimits2[0], pos2)
            if (hasAdded[pos1+1][pos2+1] and
                floatgte(currentDensity1,minDensity ) and
                floatgte(currentDensity2,minDensity) and (
                    currentCnt > maxCnt or
                    currentCnt == maxCnt and
                        floatgte(currentDensity1,maxDensity1) and
                        floatgte(currentDensity2,maxDensity2)
                    )
                ):
                maxDensity1 = currentDensity1
                maxDensity2 = currentDensity2
                maxCnt = currentCnt
                maxPos = (pos1+1, pos2+1)
                itersNotUpdated = 0

                
    innerCnt = maxCnt
    
    matches = []
    while maxPos!=(None,None):
        matches.append((maxPos[0]-1,maxPos[1]-1) # here too, revert the +1 on the indices
                       )
        maxPos = prevLink[maxPos[0]][maxPos[1]]

    matches.reverse()
    return matches

if __name__ == "__main__":   
    import doctest
    doctest.testmod()