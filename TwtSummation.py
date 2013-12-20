__author__ = 'Kaiqun'

from Freqencycounting import PunkRemovement


def tweetScoreCalcu(tweet):
    """
	:param tweet: single targeted tweet
	:return: the summed score for each tweet
	"""
    ScoreMappingDict = {}
    for item in open('res/Weights/weights.ddottwt', 'r'):
        ScoreMappingDict.update({item.split('\t')[0]: item.split('\t')[1]})
    summedScore = 0.0
    for token in tweet.strip().lower().split():
        try:
            if PunkRemovement(token) in ScoreMappingDict.keys():
                summedScore += float(ScoreMappingDict[PunkRemovement(token)])
        except Exception, e:
            print 'wrong'

    return summedScore, 'WordsWeights'


def twtStaScoreCalcu(tweetSta):
    """
	:param tweet: single targeted tweet
	:return: the summed score for each tweet
	"""
    ScoreMappingDict = {}  # Dictionary Declaration
    repeatlist = [] # declaration of list
    for item in open('res/Weights/weights.ddottwt', 'r'):
        ScoreMappingDict.update({item.split('\t')[0]: item.split(',')[1]})
    summedScore = 0.0

    for token in tweetSta.text.strip().lower().replace('\n', '').replace('\r', '').split():
        try:
            if PunkRemovement(token) in ScoreMappingDict.keys():
                if token not in repeatlist:
                    summedScore += float(ScoreMappingDict[PunkRemovement(token)])
                    repeatlist.append(token)
        except Exception, e:
            print 'wrong'

    return summedScore, 'WordsWeights'



