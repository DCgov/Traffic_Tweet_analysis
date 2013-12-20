__author__ = 'Kaiqun'

from Freqencycounting import PunkRemovement


def Str2KList(inputString, KeywordsList=[]):
    if len(KeywordsList) is 0:
        KeywordsList = [item.strip().split('\t')[0] for item in open('res/Weights/weights.ddottwt', 'r')]
    RsltList = []
    for token in inputString.strip().lower().split():
        try:
            inSertToken = PunkRemovement(token)
            if inSertToken in KeywordsList:
                if inSertToken not in RsltList:
                    RsltList.append(inSertToken)  #the code inserted prevents repeated words
        except Exception, e:
            print 'wrong'
    return RsltList
