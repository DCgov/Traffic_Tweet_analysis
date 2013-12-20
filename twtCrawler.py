__author__ = 'Kaiqun Fu and Rakesh Nune'

import twitter
import time
import DB_Connection
import json
from time import gmtime, strftime
from TwtSummation import twtStaScoreCalcu
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pytz

#TwitterAccountPool = [line.strip() for line in open('res/AccountsLists/TwitterAccountList', 'r')]
TwitterAccountPool = [line.strip() for line in open('res/AccountsLists/twitter_Account.txt', 'r')]

#KeyWordsList = [oneWord.strip() for oneWord in open('res/Kwds/TargetKey', 'r')]
#
#OverAllCount = 0


class StatusRecorder:
    def __init__(self, KeyWordsList):
        self.AccountToken = 0
        self.KeywordToken = 0
        self.KWL = KeyWordsList
        self.KWlen = len(self.KWL)

    def NextAcc(self):
        self.AccountToken = (self.AccountToken + 1) % AccCount()

    def NextKey(self):
        self.KeywordToken = (self.KeywordToken + 1) % self.KWlen

    def UpdateKeywordList(self, inputList):
        self.KWL = inputList
        self.KWlen = len(inputList)


def NextAccount(AccNum):
    api = twitter.Api(
        consumer_key=TwitterAccountPool[AccNum].split('\t')[0],
        consumer_secret=TwitterAccountPool[AccNum].split('\t')[1],
        access_token_key=TwitterAccountPool[AccNum].split('\t')[2],
        access_token_secret=TwitterAccountPool[AccNum].split('\t')[3]
    )
    return api


def AccCount():
    count = 0
    #thefile = open('res/AccountsLists/TwitterAccountList', 'rb')
    thefile = open('res/AccountsLists/twitter_Account.txt', 'rb')
    while 1:
        buffer = thefile.read(65536)
        if not buffer: break
        count += buffer.count('\n')
    return count + 1


def outputDataBase(MethodIndex, ApiResult):
    """

	:param MethodIndex: set to '0' connect to Microsoft SQL Server; set to '1' connect to MySQL Server
	"""
    if MethodIndex is 0:
        DB_Connection.MS_SqlServer_Method(ApiResult)
    elif MethodIndex is 1:
        DB_Connection.MY_SQL_Method(ApiResult)
    else:
        print 'DB connection doesn\'t exist'


def SendingEmail(Error):
    host = "smtp.gmail.com"
    port = 465
    sender = "fukaiqun.develop@gmail.com"
    pwd = "dergott22063202"
    receiver = "fukaiqun@vt.edu"

    body = "<h1>Program Stopped at " + str(datetime.now()) + "</h1>"
    body += "<h3>Here is the detailed error information: </h3>"
    body += "<p>" + Error + "</p>"
    msg = MIMEText(body, "html")
    msg["subject"] = "Program Stopped!!!!"
    msg["from"] = sender
    msg["to"] = receiver

    s = smtplib.SMTP_SSL(host, port)
    s.set_debuglevel(1)
    s.login(sender, pwd)
    s.sendmail(sender, receiver, msg.as_string())


def TwitterCrawling():
    """
	This function enables crawling Tweets with a list of Twitter application accounts and a keywords list.

	"""
    KeyWordsList = [oneWord.strip() for oneWord in open('res/Kwds/TargetKey', 'r')]
    ApiMonitor = StatusRecorder(KeyWordsList)

    OverAllCount = 0
    while True:
        try:
            TwitterApiInstance = NextAccount(ApiMonitor.AccountToken)
            OverAllCount = 0
            Xcordi = 38.907265
            Ycordi = -77.03649
            while True:

                temp = TwitterApiInstance.GetSearch(term=ApiMonitor.KWL[ApiMonitor.KeywordToken], lang='en', count=100,
                                                    geocode=(Xcordi, Ycordi, '20mi'))
                temp1 = TwitterApiInstance.GetSearch(term='#dctraffic OR #vatraffic OR #mdtraffic')
                ApiMonitor.NextKey()
                time.sleep(0.3)
                DB_Connection.MongoDB_Insertion(temp)
                DB_Connection.MongoDB_Insertion(temp1)
                OverAllCount += 1
                if datetime.now(pytz.timezone('US/Eastern')).strftime('%H:%M') == '02:10':
                    ApiMonitor.UpdateKeywordList([oneWord.strip() for oneWord in open('res/Kwds/TargetKey1', 'r')])
                    time.sleep(61)
                    print 'Awake'
                pass

        except Exception, e:
            global OverAllCount
            if e.__class__.__name__ is 'TwitterError':
                Errotype = e.message[0]['code']
                if Errotype is 88:
                    ApiMonitor.NextAcc()
                    print 'Switch Account! Next Account:' + str(
                        ApiMonitor.AccountToken) + '  Total queries sent:' + str(OverAllCount) + '    ' + datetime.now(
                        pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    print str(e)
            else:
                print "SERIOUS ERROR! ======> " + str(e)


if __name__ == '__main__':
    try:
        TwitterCrawling()
    except Exception, e:
        SendingEmail(str(e))