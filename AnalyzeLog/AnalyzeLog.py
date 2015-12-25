# -*- coding:utf-8 -*-
import os
import sys
import re
import threading
import time

filterList = []
filterMap = {}

g_strInfo = re.compile('[:|^|;|=]')


def CheckString(srcName, filePath):
	try:
		logFile = open(filePath, 'r')
	except Exception as e:
		print e, filePath
		return

	try:
		start = time.clock()

		for line in logFile:
			for filterStr in filterList:
				if -1 != line.find(filterStr):
					DoneTargetFile(srcName, filePath, filterStr)
					pass

		end = time.clock()
		print end - start
	except Exception as e:
		print e, filePath

	logFile.close()
	return 

def ReadFilterString(filePath):
	for line in open(filePath):
		if '\n' == line[-1]:
			filterList.append(line[:-1])
			filterMap[line[:-1]] = 0
		else:
			filterList.append(line)
			filterMap[line] = 0
		
	return 

def DoneTargetFile(srcName, srcPath, filterString):
	
	fileName = g_strInfo.sub(' ', filterString)
	filterMap[filterString] += 1

	targetDir = g_outDir + "\\" + fileName;
	if False == os.path.isdir(targetDir):
		os.makedirs(targetDir)

	targetPath = targetDir + "\\" + srcName;

	try:
		targetFile = open(targetPath, "w")
	except IOError as e:
		print e, targetPath
		return

	try:
		targetFile.write(open(srcPath).read())
	except IOError as e:
		print e, targetPath

	targetFile.close()
	return

def RunThread(dirPath, fileList):
	for fileName in fileList:
		filePath = dirPath + "\\" + fileName
		#if False == os.path.isfile(filePath):
		#	continue
		CheckString(fileName, filePath)
	return

def ScanDir(dirPath, exceptionName):
	if False == os.path.isdir(dirPath):
		print dirPath, "isn't a directory's path."
		return

	threadLst = []
	fileNames = os.listdir(dirPath)

	nThdCount = 5
	nFileCount = len(fileNames)

	if nThdCount > nFileCount:
		nThdCount = nFileCount

	for i in range(0, nThdCount):
		startPos = i*nFileCount/nThdCount
		endPos = (i+1)*nFileCount/nThdCount

		if i+1 != nThdCount:
			t = threading.Thread(target=RunThread, args=(dirPath, fileNames[startPos:endPos], ))
		else:
			t = threading.Thread(target=RunThread, args=(dirPath, fileNames[startPos:], ))
		threadLst.append(t)

	for t in threadLst:
		t.start()

	for t in threadLst:
		t.join()
	
	return

#########################Begin####################
argsCount = len(sys.argv)
if 4 != argsCount:
	print u"Usage:Input a source dir path , a filter file path and output dir."
	sys.exit()

#########################Analyze paramters###############
g_srcDir = sys.argv[1]
g_filterFilePath = sys.argv[2]
g_outDir = sys.argv[3]

if False == os.path.isdir(g_outDir):
	os.makedirs(g_outDir)

##########################Read filter string##################
ReadFilterString(g_filterFilePath)
if 0 == len(filterList):
	print u"Cannot find a file:", g_filterFilePath
	sys.exit()

##########################Working##############################
g_start = time.clock()

ScanDir(g_srcDir, "")

g_end = time.clock()

############################Result###############################
print u"Using:", g_end - g_start, u"second"
print u"Result:"
for k,v in filterMap.items():
	print k,":", v

