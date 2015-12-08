# -*- coding:utf-8 -*-
import os
import sys
def AddEndFlag(path, tagEndName):
	try:
		logFile = open(path, 'a+')
		lines = logFile.read()

		if -1 == lines.find(tagEndName):
			logFile.seek(0, 2)
			logFile.write('\r\n')
			logFile.write(tagEndName)
			logFile.write('\r\n')

		logFile.close()

	except Exception as e:
		print e, path

	return

def ScanDirAndAddFlag(dirPath, flagName, exceptionName):
	if False == os.path.isdir(dirPath):
		print dirPath, "isn't a directory's path."
		return

	fileNames = os.listdir(dirPath)
	for fileName in fileNames:
		path = dirPath + "\\" + fileName
		if False == os.path.isfile(path):
			continue

		if 0 == cmp(fileName, exceptionName):
			continue

		AddEndFlag(path, flagName)
	return

count = len(sys.argv)
if 4 == count:
	ScanDirAndAddFlag(sys.argv[1], sys.argv[2], sys.argv[3])
else:
	print "Input a dir path, flag and exception file name."
