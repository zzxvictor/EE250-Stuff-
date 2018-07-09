#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 21:24:57 2018

@author: victorzhang
"""

#read json file one by one, remove invalid data
#valid data are added to a csv file
import json 
import os
import pandas 
import sys
import glob
import numpy as np
import re


columnNames = ['jobID', 'jobTitle', 'keywordUsedInSearch','jobLocation', 'locationFilterUsedInSearch',  'rating', 'estimatedWage', 'jobDescription', 'companySize',
               'companyRevenue', 'companyIndustryField', 'companyWebsite', 'companyType', 'companyCompetitors' , 'companyHeadQuarter', 'foundedTime']
def readFileNames (folder):
    #if path does not exist
    if not os.path.isdir(folder) :
        print ('ERROR! Input folder does not exist')
        sys.exit()
    else:
        return glob.glob(folder + '/*_raw.json')
         
def loadJSON (fileName):
    with open(fileName) as jsonFile:
        jsonData = json.load(jsonFile)
    return jsonData

def loadCSV(csvPath):
    global columnNames
    #check if the file exist
    if os.path.isfile(csvPath):
        return pandas.read_csv(csvPath)
    else:
    #if not exist, create an empty csv file
        df = pandas.DataFrame(columns = columnNames)
        return df
    
def checkValidity (jsonFile):
    # if the string is shorted than 100 charactors, it should be discarded
    if jsonFile['jobDescription'] is None or len(jsonFile['jobDescription']) < 100:
        return False
    else:
        return True
    
def addToCSV(jsonFile,file, df):
    global columnNames 
    fileName = file.split('/')[-1]
    keywordUsed = ' '.join (fileName.split('_')[0].split('-')[:-1])
    locationFilterUsed = fileName.split('_')[0].split('-')[-1]
    jobID = jsonFile['jobID']
    jobTitle = jsonFile['jobTitle']
    #check validity 
    checkPattern1 = 'data'
    if re.search(checkPattern1, jobTitle.lower()) is None:
        return df
    jobLocation = jsonFile['jobLocation']
    rating = jsonFile['companyRating']
    wage = jsonFile['estimatedSalary']
    jobDescription = jsonFile['jobDescription']
    
    

    try:
        companySize = jsonFile['companyInfo']['Size']
    except:
        companySize = None 
    try:
        revenue = jsonFile['companyInfo']['Revenue']
    except:
        revenue = None 
    try:
        industry = jsonFile['companyInfo']['Industry']
    except:
        industry = None 
    try:
        companyWeb = jsonFile['companyInfo']['Website']
    except:
        companyWeb = None
    try:
        companyType = jsonFile['companyInfo']['Type']
    except:
        companyType = None
    try:
        competitors = jsonFile['companyInfo']['Competitors']
    except:
        competitors = None
    try:
        headQuarter = jsonFile['companyInfo']['Headquarters']
    except:
        headQuarter = None
    try:
        foundedTime = jsonFile['companyInfo']['Founded']
    except:
        foundedTime = None 
    #clean out irrelevant jobs 
    
    row = [jobID, jobTitle, keywordUsed, jobLocation, locationFilterUsed, rating, wage, jobDescription,
           companySize, revenue, industry, companyWeb, companyType, competitors, headQuarter, foundedTime]
    newDf = pandas.Series(row, index = columnNames)
    df = df.append(newDf, ignore_index = True)
    return df


def saveCSV(outPath, df, name):
    if not os.path.isdir(outPath):
        os.mkdir (outPath)
    fileName = outPath + '/' + name
    df.to_csv(fileName, index = False)
    print ('done!')
    
def main():
    inPath = '/Users/victorzhang/Desktop/rawData/glassdoor_wave2'
    outPath = '/Users/victorzhang/Desktop/preprocessed'
    csvFileName = 'preprocessedData2.csv'
    df = loadCSV(outPath+'/'+csvFileName)
    fileList = readFileNames(inPath)
    for file in fileList:
        jsonFile = loadJSON(file)
        if checkValidity(jsonFile):
            df = addToCSV(jsonFile, file, df)
    
    saveCSV(outPath, df, csvFileName)
    
main()