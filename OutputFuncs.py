__author__ = 'Kaiqun'

import time

# This file contains all the functions needed for the project's output.

def outputConsole(ApiResult, kword):
	"""
	This function outputs the results in the console
	:param ApiResult: a twitter api status object
	:param kword: the keyword that the api result get from
	"""
	for tmp in ApiResult:
		print tmp.text.strip().replace('\n', ' ').replace('\r', ' ') + ' -----> ' + kword


def outputFile(ApiResult, outputFile):
	"""
	This function ouputs the results in the file whose path is assigned by :param outputPath
	:param ApiResult: a twitter api status object
	:param outputPath: the output path for the output file
	"""
	WriterFile = open('Results/' + time.strftime("%d-%m-%Y") + '/' + outputFile, 'a')
	for one in ApiResult:
		WriterFile.write(
			one.created_at + '\t' + one.user.screen_name + '\t' + one.text.encode('UTF-8').strip().replace('\n', ' ').replace('\r', ' ') + '\n')