#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:22:07 2018

@author: victorzhang
"""

import pandas
import glob
import os 
import sys

def readFileNames (folder):
    #if path does not exist
    if not os.path.isdir(folder) :
        print ('ERROR! Input folder does not exist')
        sys.exit()
    else:
        return glob.glob(folder + '/preprocesse*.csv')
    
def concatenate (fileList):
    print ('need implementation')


def loadCSV(csvPath):
    global columnNames
    #check if the file exist
    if os.path.isfile(csvPath):
        return pandas.read_csv(csvPath)
    else:
    #if not exist, create an empty csv file
        df = pandas.DataFrame(columns = columnNames)
        return df
    
def saveCSV(outPath, df, fileName):
    if not os.path.isdir(outPath):
        os.mkdir (outPath)
    fileName = outPath + '/' + fileName
    df.to_csv(fileName, index = False)
    print ('done!')
    
def main():
    inputFolder = '/Users/victorzhang/Desktop/preprocessed'
    outputFolder = '/Users/victorzhang/Desktop/preprocessed'
    newFileName = 'finalPreprocessed.csv'
    fileList = readFileNames(inputFolder)
    aggregate = loadCSV(fileList[0])    
    for file in fileList[1:]:
        df2 = loadCSV(file)
        aggregate = pandas.concat([df2,aggregate], ignore_index = True)
    
    uniqueDF = aggregate.drop_duplicates(subset = ['jobID'], keep = 'first').reset_index(drop = True)
    saveCSV(outputFolder, uniqueDF, newFileName)
    
main()
    