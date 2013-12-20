__author__ = 'Kaiqun'

import pymongo
from Freqencycounting import frequencounting4Up, FrequencyCalcu4Up
import datetime, calendar, time
import pytz
from collections import namedtuple


def TermWeightUper(inputClct):
    mongodb_uri = 'mongodb://localhost:27017'
    db_name = 'TwitterData'
    db_collection = inputClct

    try:
        connection = pymongo.Connection(mongodb_uri)
        database = connection[db_name]
        tmpCollct = database[db_collection]
    except:
        print('Error: Unable to connect to database.')
        connection = None

    if connection is not None:
        TextList = [oneDoc['text'].encode('UTF-8').replace('\n', '').replace('\r', '').strip() for oneDoc in
                    tmpCollct.find({"retweeted_status": {"$not": {"$exists": "true"}}}) if
                    oneDoc['pj_scoreObj'][0]['score_num'] > 3.1]
        return frequencounting4Up(TextList)
    return 'Connection None'


Task = namedtuple("task", "name, time, task")


def perfrom_one_task(task=None):
    Yesterday = datetime.datetime.now(pytz.timezone('US/Eastern')) + datetime.timedelta(days=-1)
    UTCstamp = calendar.timegm(Yesterday.utctimetuple())
    time_str = Yesterday.strftime('%H:%M')
    if time_str == task.time:
        print "Performing", task.name
        clctName = datetime.datetime.fromtimestamp(int(UTCstamp)).strftime('%d-%b-%Y')
        task.task(clctName)
        time.sleep(70)
        print "Sleep Done!"
        return True
    return False


def run(Tasks):
    while True:
        map(perfrom_one_task, Tasks)
        time.sleep(1)

# ==============================================================================


def mytask(clctName='04-Sep-2013'):
    WTcontent = '#dctraffic' + '\t' + '100.0' + '\n' + '#mdtraffic' + '\t' + '100.0' + '\n' + '#vatraffic' + '\t' + '100.0' + '\n' + '\n'.join(
        [i[0] + '\t' + str(i[1]) for i in FrequencyCalcu4Up(TermWeightUper(clctName), 150)])
    KWcontent = '#dctraffic' + '\n' + '#mdtraffic' + '\n' + '#vatraffic' + '\n' + '\n'.join(
        [i[0] for i in FrequencyCalcu4Up(TermWeightUper(clctName), 75)])
    WritingFile = open('res/Weights/' + clctName + '_weights.ddottwt', 'w')
    WritingFile.write(WTcontent)
    WritingFile.close()
    WritingFile = open('res/Weights/weights.ddottwt', 'w')
    WritingFile.write(WTcontent)
    WritingFile.close()
    WritingFile = open('res/Kwds/' + clctName + '_Keywords.ddottwt', 'w')
    WritingFile.write(KWcontent)
    WritingFile.close()
    WritingFile = open('res/Kwds/TargetKey1', 'w')
    WritingFile.write(KWcontent)
    WritingFile.close()


Tasks = [Task("TermUpdating", "02:00", mytask)]

run(Tasks)