__author__ = 'Kaiqun'

from nltk.corpus import stopwords
from collections import Counter
import string

table = string.maketrans("", "")


def frequencounting(Listings):
    """
	Get the keywords count and the rank of the keywords
	:param Listings: the input list of tweets
	:return: a list of tuple ranked by words counts
	"""
    MyCounter = Counter()
# This function is used to count the number of words in the tweets from the influential users from input list
    chars = ['.', '/', "'", '"', '?', '!', '#', '$', '%', '^', '&',
             '*', '(', ')', ' - ', '_', '+', '=', '@', ':', '\\', ',',
             ';', '~', '`', '<', '>', '|', '[', ']', '{', '}', '-', '"', '&amp;', 'rt']

    # This section below will filter out the common english words and punctuations from the target tweets.
    for line in Listings:
        for word in line.text.encode('UTF-8').strip().lower().split():
            if PunkRemovement(word.strip().lower()) not in chars + stopwords.words('english'):
                MyCounter[PunkRemovement(word.strip().lower())] += 1

    TempStoring = MyCounter.most_common()
    for (key, val) in FrequencyCalcu(TempStoring):
        try:
            print str(key.decode('UTF-8')) + '\t' + str(val)
        except:
            pass
    return TempStoring


def frequencounting4Up(Listings):
    """
	Get the keywords count and the rank of the keywords
	:param Listings: the input list of tweets
	:return: a list of tuple ranked by words counts
	"""
    MyCounter = Counter()

    chars = ['.', '/', "'", '"', '?', '!', '#', '$', '%', '^', '&',
             '*', '(', ')', ' - ', '_', '+', '=', '@', ':', '\\', ',',
             ';', '~', '`', '<', '>', '|', '[', ']', '{', '}', '-', '"', '&amp;', 'rt']

    UpdatingChars = ['&amp;', 'rt', '', '#dctraffic', '#mdtraffic', '#vatraffic', 'amp', '-']

    # This section below will filter out the common english words and punctuations from the target tweets.
    for line in Listings:
        if type(line) is str:
            for word in line.strip().lower().split():
                if PunkRemovement(word.strip().lower()) not in UpdatingChars + stopwords.words(
                        'english') and not word.isdigit():
                    if len(word) > 1:
                        MyCounter[PunkRemovement(word.strip().lower())] += 1
        else:
            for word in line.text.decode('UTF-8').strip().lower().split():
                if PunkRemovement(word.strip().lower()) not in chars + stopwords.words('english'):
                    MyCounter[PunkRemovement(word.strip().lower())] += 1

    return MyCounter.most_common()


def frequencountingFile(Listings):
    """
	Get the keywords count and the rank of the keywords
	:param Listings: the input list of tweets
	:return: a list of tuple ranked by words counts
	"""
    MyCounter = Counter()

    chars = ['.', '/', "'", '"', '?', '!', '#', '$', '%', '^', '&',
             '*', '(', ')', ' - ', '_', '+', '=', '@', ':', '\\', ',',
             ';', '~', '`', '<', '>', '|', '[', ']', '{', '}', '-', '"', '&amp;', 'rt', '#dctraffic', '#mdtraffic',
             '#vatraffic']

    # This section below will filter out the common english words and punctuations from the target tweets.
    for line in Listings:
        for word in line.split('\t')[2].decode('UTF-8').encode('UTF-8').strip().lower().split():
            if PunkRemovement(word.strip().lower()) not in chars + stopwords.words('english'):
                MyCounter[PunkRemovement(word.strip().lower())] += 1

    TempStoring = MyCounter.most_common()
    for (key, val) in TempStoring:
        try:
            print str(key.decode('UTF-8')) + '\t' + str(val)
        except:
            pass
    return TempStoring


def PunkRemovement(inputStr):
    """
	This is a support function to remove the punctuations in the keywords
	:param inputStr: the target string that contains all unwanted punctuations
	:return:
	"""
    return inputStr.translate(table, string.twtpunctuation)


def FrequencyCalcu(TupleList):
    TotalCounts = 0.0
    TempDiction = {}
    for item in TupleList:
        TotalCounts += item[1]

    for one in TupleList:
        TempDiction.update({one[0]: one[1]})

    OutputTupList = []
    for item in open('D:\GDrive\Twitter_Sentiment_Ana\Results\TermFrequency_Resullt\NewResultTop20.csv', 'r'):
        OutputTupList.append((item.split(',')[0], (float(item.split(',')[1]) / TotalCounts) * 100))

    return OutputTupList


def FrequencyCalcu4Up(TupleList, length):
    TotalCounts = 0.0
    TempDiction = {}
    for item in TupleList:
        TotalCounts += item[1]

    for one in TupleList:
        TempDiction.update({one[0]: one[1]})

    OutputTupList = []
    for item in TupleList[:length]:
        OutputTupList.append((item[0], (float(item[1]) / TotalCounts) * 100))

    return OutputTupList


def recentDoc2Dic(filePath):
    RsltDict = {}
    for line in open(filePath, 'r'):
        RsltDict.update({line.split('\t')[0]: float(line.split('\t')[1].strip())})
    return RsltDict


def FrequencyCalcuDictInput(inputDict):
    TotalCounts = 0.0
    for val in inputDict:
        TotalCounts += inputDict[val]

    OutputTupList = []
    for val in inputDict:
        OutputTupList.append(((inputDict[val] / TotalCounts) * 100, val))

    OutputTupList = sorted(OutputTupList, reverse=True)

    for item in OutputTupList:
        try:
            print str(item[1].decode('UTF-8')) + '\t' + str(item[0])
        except:
            pass

    # print OutputTupList
    return OutputTupList