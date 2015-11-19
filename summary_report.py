#!/usr/bin/python
import os
import sys
import csv
import shutil
import subprocess
import string
import gzip
import glob
from os import walk

"""
__module__: summary_report
__author__: "Prateek Kumar"
__description__: This module extracts specified data from the given directory.
__copyright__: "Minesense"
"""

#Global declaration of variables.

fileList=list()   
CuADict=dict()
CuBDict=dict()
DecDict=dict()
CuADictBlu = dict()
CuBDictBlu = dict()


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

def reporting_logs(log_dir):
    files=[]
    list_gz_files=[]
    savedPath=os.getcwd()
    #log_path is the complete path of the directory containing the logs.
    log_path = os.path.normpath(os.path.join( os.getcwd(),log_dir) )
    if os.path.exists(log_path):
        print "reached inside the file"
        for (dir,dirnames,filenames) in walk(log_path):
            for file in filenames:
                file_path=os.path.join(dir,file)
                file_path=os.path.normpath(file_path)
                files.append(file_path)

    """
    Decompressing the .gz files in the given directory and extracting the information
    from the file.
    """
    os.mkdir("output_logs")
    output_path = os.path.normpath(os.path.join( os.getcwd(),"output.csv") )           
    for file in files:
        if file.endswith('.gz'):
            with gzip.open(file, 'rb') as gz_file:
                file_lines=gz_file.readlines()
                with open('output.csv','w') as output_file:
                    output_file.writelines(file_lines)
            extract_info(file,output_file)

        if file.endswith('.0'):
            with open(file,'rb') as cur_file:
                lines=cur_file.readlines()
                with open('output.csv','w') as output_file:
                    output_file.writelines(lines)
            extract_info(file,output_file)

    summary_table=open('summary_table.csv','w+')
    summaryWriter = csv.writer(summary_table,delimiter = ',')
    
    csvRow = list()
    
    csvRow.append("Project")
    csvRow.append("Sample")
    csvRow.append("Run")
    csvRow.append("WND_Start")
    csvRow.append("WND_Stop")
    csvRow.append("WND_Width")
    csvRow.append("CukA_Avg")
    csvRow.append("CukB_Avg")
    csvRow.append("DEC")
    
    summaryWriter.writerow(csvRow)
    for file in fileList:
        csvRow =list()
        csvRow.append(project_name[file])
        csvRow.append(sample[file])
        csvRow.append(run[file])
        csvRow.append(WND_Start[file])
        csvRow.append(WND_Start[file])
        csvRow.append(CuADictBlu[file])
        csvRow.append(CuBDictBlu[file])
        csvRow.append(DecDict[file])
        summaryWriter.writerow(csvRow)
    summary_table.close()
    

def extract_info(file_name, output_file_path):
    """
    This function will be used to extract information from the file.
    """
    fileList=list()
    project=dict()
    sample=dict()
    run=dict()
     
    CuADict=dict()
    CuBDict=dict()
    DecDict=dict()
    CuADictBlu = dict()
    CuBDictBlu = dict()
    
    fileList.append(file_name)

    if os.path.isfile(output_file_path):
        with open('output_file_path') as csvfile:
            testFiles=csv.reader(csvfile)
            for row in testfile:
                CuA = float(row[1])
                CuB = float(row[2])
                
                CuADict[file_name] = CuA
                CuBDict[file_name] = CuB
                
                CuADictBlu[file_name] = getValue(output_file_path, 'CuAlpha')
                CuBDictBlu[file_name] = getValue(output_file_path, 'CuBeta')
                DecDict[file_name] = getDecision(output_file_path).rstrip()
    else:
        print "Output file is not created yet."
        

if __name__ =="__main__":
    reporting_logs("Downloads")
    
