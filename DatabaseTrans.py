import os
import pymongo
import unicodedata
import ast
import json
import time
import calendar
from String2KwdList import Str2KList
from TwtSummation import tweetScoreCalcu

# writingFile = open()

def writingResults(dateIndex, Kword):
    TotalCount = 0
    mongodb_uri = 'mongodb://localhost:27017'
    db_name = dateIndex
    clt_name = Kword
    count = 0

    # try:
    connection = pymongo.Connection(mongodb_uri)
    database = connection[db_name]
    Collect = database[Kword]
    for one_twt in Collect.find({"retweeted_status": {"$not": {"$exists": "true"}}}):
        # print one_twt.keys()
        count += 1
        print one_twt['text'].encode('UTF-8').strip().replace('\n', '').replace('\r', '') + '  ===>  ' + \
              one_twt['user']['screen_name'].encode('UTF-8')
    # except Exception, e:
    # 	print e.message
    print count


def ExtractNegSet(dateIndex):
    mongodb_uri = 'mongodb://localhost:27017'
    db_name = dateIndex
    count = 0
    writingFile = open('NegSet_Raw.txt', 'a')

    # try:
    connection = pymongo.Connection(mongodb_uri)
    database = connection[db_name]
    for clct_name in [tempone for tempone in database.collection_names() if tempone not in ['system.indexes']]:
        print clct_name
        one_Collect = database[clct_name]
        # for one_twt in one_Collect.find({"retweeted_status": {"$not": {"$exists": "true"}}}):
        for one_twt in one_Collect.find():
            # print one_twt.keys()
            count += 1
            # print one_twt['text'].encode('UTF-8').strip().replace('\n', '').replace('\r', '') + '  ===>  ' + one_twt['user']['screen_name'].encode('UTF-8')
            print one_twt
        # except Exception, e:
        # 	print e.message
    print count


def DataTransmition(Targ_db_name):
    mongodb_uri = 'mongodb://localhost:27017'
    stop_db_names = ['local', 'TwitterData', 'edda', 'names']
    stop_clct_names = ['system.indexes']

    KeywordsList = [item.strip().split('\t')[0] for item in open('res/Weights/weights.ddottwt', 'r')]

    connection = pymongo.Connection(mongodb_uri)
    for one_db_name in [valid_n for valid_n in connection.database_names() if valid_n not in stop_db_names]:
        database = connection[one_db_name]
        for clct_name in [valid_n for valid_n in database.collection_names() if valid_n not in stop_clct_names]:
            one_Collect = database[clct_name]
            for document in one_Collect.find():
                methodList = []
                (Score, Method) = tweetScoreCalcu(
                    document['text'].encode('UTF-8').replace('\n', '').replace('\r', '').strip())
                methodList.append({"method": Method, "score_num": Score})
                document.update({
                    "pj_kwdlist": Str2KList(document['text'].encode('UTF-8').replace('\n', '').replace('\r', '').strip(),
                                            KeywordsList=KeywordsList)})
                document.update({"pj_scoreObj": methodList})
                tmpDB = connection[Targ_db_name]
                tmpCollct = tmpDB[
                    time.strftime("%d-%b-%Y", time.strptime(document['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))]
                try:
                    tmpCollct.insert(document)
                except Exception, e:
                    print str(e)
                    return 'Crap!'


if __name__ == '__main__':
    DataTransmition('TwitterData')