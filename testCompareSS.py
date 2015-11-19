#!/usr/bin/python
import os
import sys
import csv
import shutil
import subprocess
import string


def trimString(inputS):
    all = string.maketrans('','')
    nodigs = all.translate(all, string.digits)
    inputS = inputS.translate(all, nodigs)
    return inputS

def getValue(entry, key):
    resFile = open(entry,"r")
    for line in resFile:
        #print line
        if line.find(key) != -1:
            sep = line.find(":")
            if sep != -1:
                val = line[sep+1:].split()[0]
                #print "Value: " + val
                return float(val)

def getDecision(entry):
    resFile = open(entry,"r")
    for line in resFile:
        #print line
        if line.find('Decision') != -1:
            sep = line.find(":")
            if sep != -1:
                val = line[sep+2:]
                #print "Value: " + val
                return val
    return "NO WINDOW"

if __name__=="__main__":
    testResults = os.path.normpath(os.path.join( os.getcwd(),"test-results") )
    fileList = list()
    CuADict = dict()
    CuBDict = dict()
    CuADictBlu = dict()
    CuBDictBlu = dict()
    MatDict = dict()
    DecDict = dict()

    with open('dataFileList_SS.csv', 'rb') as csvfile:
        testFiles = csv.reader(csvfile)
        for row in testFiles:
            fileName = os.path.basename(row[0])
            resultFileName = os.path.normpath(os.path.join(testResults, fileName+".log.res"))
            CuA = float(row[1])
            CuB = float(row[2])
            
            if (os.path.isfile(resultFileName)):
                fileList.append(resultFileName)
                CuADict[resultFileName] = CuA
                CuBDict[resultFileName] = CuB
                CuADictBlu[resultFileName] = getValue(resultFileName, 'CuAlpha')
                CuBDictBlu[resultFileName] = getValue(resultFileName, 'CuBeta')
                DecDict[resultFileName] = getDecision(resultFileName).rstrip()
                MatDict[resultFileName] = row[25]
            else:
                print "Does not exist : %s"%resultFileName


    comparisonFile = open("comparision.csv","w+")
                
    comparisonWriter = csv.writer(comparisonFile, delimiter = ',')
    

    csvRow = list()
    csvRow.append("File")
    csvRow.append("Johns CuA")
    csvRow.append("Blus CuA")
    csvRow.append("Difference in CuA")
    csvRow.append("Johns CuB")
    csvRow.append("Blus CuB")
    csvRow.append("Difference in CuB")
    csvRow.append("Material")
    csvRow.append("Decision")

    
    comparisonWriter.writerow(csvRow)

    for resFile in fileList:

        csvRow = list()
        csvRow.append(resFile)
        csvRow.append(CuADict[resFile])
        if(CuADictBlu[resFile] != None):
            csvRow.append(CuADictBlu[resFile])
            csvRow.append(CuADict[resFile] - CuADictBlu[resFile])
        else:
            csvRow.append('0')
            csvRow.append('0')
        csvRow.append(CuBDict[resFile])
        if(CuBDictBlu[resFile] != None):
            csvRow.append(CuBDictBlu[resFile])
            csvRow.append(CuBDict[resFile] - CuBDictBlu[resFile])
        else:
            csvRow.append('0')
            csvRow.append('0')
        csvRow.append(MatDict[resFile])
        csvRow.append(DecDict[resFile])
        comparisonWriter.writerow(csvRow)

    comparisonFile.close()


