__author__ = 'Kaiqun'

#import MySQLdb
import pymongo
import ast
import json
import time
import calendar
from String2KwdList import Str2KList
from TwtSummation import tweetScoreCalcu
from datetime import datetime

Connection_Config = [line.strip() for line in open('res/DatabaseConfig/Connections', 'r')]


def MS_SqlServer_Method():
    conn = pymssql.connect(
        host=Connection_Config[0].split('\t')[0],
        user=Connection_Config[0].split('\t')[1],
        password=Connection_Config[0].split('\t')[2],
        database=Connection_Config[0].split('\t')[3]
    )
    cur = conn.cursor()

    cur.execute("""SELECT [IncID]
      ,[ddot_StartDate]
      ,[ddot_DetctTime]
      ,[ddot_detctSrc]
      ,[ddot_othsrc]
      ,[ddot_description]
      ,[ddot_street2]
      ,[ddot_street1]
      ,[ddot_Comments]
      ,[ddot_longitude]
      ,[ddot_latitude]
  FROM [tirs].[dbo].[Incident_ddot]""")

    row = cur.fetchone()
    while row:
        print row
        row = cur.fetchone()


def MongoDB_Insertion(inputObject):
    """

	:param inputObject: twitter status object
	:param MappingIndex:
	:param KWord: from which keyword this tweet crawled from.
	:return:
	"""
    mongodb_uri = 'mongodb://localhost:27017'
    db_name = 'TwitterData'
    db_collection = 'Washingtondc'

    KeywordsList = [item.strip().split('\t')[0] for item in open('res/Weights/weights.ddottwt', 'r')]

    try:
        connection = pymongo.Connection(mongodb_uri)
        database = connection[db_name]
        tmpCollct = database[db_collection]
    except:
        print('Error: Unable to connect to database.')
        connection = None
    #input object submitted through argument
    if connection is not None:
        for f in inputObject:
            if f.retweeted_status is not None:
                flag = 1
            else:
                flag = 0
            jsonstr = str(f)
            TempJson = json.loads(jsonstr)
            TempJson.update({"_id": TempJson['id']})
            #			print [key for key in TempJson.keys()]
            if TempJson.get('urls'):
                TempJson.update({"urls": "ILLEGAL"})
            if flag is 1:
                TempJson['retweeted_status'].update({"urls": "ILLEGAL"})
            (Score, Method) = tweetScoreCalcu(
                TempJson['text'].encode('UTF-8').replace('\n', '').replace('\r', '').strip())
            methodList = []
            methodList.append({"method": Method, "score_num": Score})
            TempJson.update({"pj_scoreObj": methodList})
            TempJson.update({
                "pj_kwdlist": Str2KList(TempJson['text'].encode('UTF-8').replace('\n', '').replace('\r', '').strip(),
                                        KeywordsList=KeywordsList)})
            TempJson.update(
                {"pj_UTCtime": calendar.timegm(time.strptime(TempJson['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))})
            tmpCollct = database[
                time.strftime("%d-%b-%Y", time.strptime(
                    datetime.fromtimestamp(int(TempJson['pj_UTCtime'])).strftime('%a %b %d %H:%M:%S %Y')))]
            # tmpCollct = database['foo']
            # Threshold value to store the data in the system
            #Made the change
            try:
                if TempJson['pj_scoreObj'][0]['score_num'] >= 2.0 and len(TempJson['pj_kwdlist']) >=3:
                    tmpCollct.insert(TempJson)
            except Exception, e:
                print e.message
                return 'Crap!'
    return 'Done'