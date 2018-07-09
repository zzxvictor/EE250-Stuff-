#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 19:46:05 2018

@author: victorzhang
"""
import urllib.error, urllib.request, urllib.parse
from bs4 import BeautifulSoup
import json
import os  
import numpy 
import sys 

def getHTML(url):
    #access glassdoor website
    req = urllib.request.Request(url, headers={'User-Agent' : "Safari's Browser"})
    #get html files
    html = urllib.request.urlopen( req ).read()
    #make a soup
    soup = BeautifulSoup(html, "html.parser")
    return soup 
def harvestLinks(nextpage, neighorpage):
    while True:
        try:
            #access web page
            soup = getHTML(nextpage)
            break
        #if a problem encountered
        except :
            try:
                soup = getHTML(neighorpage)
                break
            except:
                print ('error1')
                #unexpected error, stop (failed to load two consecutive pages )
                return -1, -1, -1 
    #next page
    try:
        nextPage = 'https://www.glassdoor.com' + soup.find('li', attrs = {'class': 'next'}).find('a', href = True)['href']
        neighborPage = 'https://www.glassdoor.com' + soup.find('li', attrs = {'class': 'page last'}).find('a', href = True)['href']
    except: 
        print ('error2')
        nextPage =  neighborPage = -1
    
    #get links to jobs (dict obj)
    dictList = soup.find_all('a', attrs = {'class': 'jobLink'}, href = True)
    linksList = []
    for item in dictList:
        linksList.append('https://www.glassdoor.com' + item['href'])
        
    return linksList, nextPage, neighborPage


def main():
    print ('Welcome to victors\'s glassdoor web crawling service')
    inputFile = '/Users/victorzhang/Desktop/inputLinks.txt'
    outputFolder = '/Users/victorzhang/Desktop/rawData/glassdoor_wave2'
    lines = [line.rstrip('\n') for line in open(inputFile)]
    #30 pages maximum
    maxi = 30
    counter = 0
    
    while counter < len(lines) -1 :
        keyWord = lines[counter]
        counter += 1
        url = lines[counter]
        counter += 1
        neighbor = ''
        
        myLinks = []
        summ = 0
        jobCounter = 0
        print ('going through ' + keyWord)
        while summ < maxi: 
            summ += 1
            print ('Accessing page No.%d' %(summ))
            links, nextPage , neighborPage = harvestLinks(url , neighbor)
            url = nextPage
            neighbor = neighborPage
            myLinks = numpy.unique(links)
            if links == -1:
                print ('reached end')
                break
            #access page 
            for link in  myLinks:
                fileName, info = collectJobInfos(link, outputFolder, keyWord)
                if fileName == 'H':
                    continue
                jobCounter += 1
                createJson(fileName, info, outputFolder)
            print ('%d jobs intotal have been found' %(jobCounter))
            
    print ('Done')
            
   
 
def collectJobInfos(jobUrl, outPath, keyWord):
    #get ID 
    jobID = jobUrl.split('=')[-1]
    fileName = outPath + '/' + str(keyWord) + '_job_' + str(jobID) + '_raw.json'
    if os.path.isfile(fileName) :
        return 'H', []
    try:
        soup = getHTML(jobUrl)
    except:
        return 'H', []
    myJob = {}
    #job ID
    myJob['jobID'] = jobID
    #extract location info
    location = soup.find('span', attrs = {'class':'subtle ib'}).text.split()[1:]
    try:
        location[-2] = location[-2][:-1]
    except:
        location = 'None'
    location = '_'.join (location)
    myJob['jobLocation'] = location
    #extract job name
    try:
        title = soup.find('h2', attrs = {'class':'noMargTop margBotXs strong'}).text
    except:
        title = 'None'
    myJob['jobTitle'] = title
    myJob['jobLocation'] = location
    #find rating 
    try:
        rating = soup.find('div', attrs = {'class':'ratingNum'}).text
    except:
        rating = None
    myJob['companyRating'] = rating
    
    #find company information 
    try:
        info = {}
        companyInfo = soup.find_all('div', attrs = {'class':'infoEntity'})
        for item in companyInfo:
            info[item.find('label').text] = item.find('span').text
    except:
        companyInfo = {}
    myJob['companyInfo'] = info
    
    #find salary expectation 
    try:
        salary = soup.find('h2', attrs = {'class':'salEst'}).text.split('/')[0][1:].replace(',', '')
    except:
        salary = None 
    myJob['estimatedSalary'] = salary
    
    #job description 
    try:
        jobDescription = soup.find('div', {'class': 'jobDescriptionContent desc module pad noMargBot'}).text
    except:
        jobDescription = ''
    myJob['jobDescription'] = jobDescription
    
    #create fileName
    return fileName, myJob
    
    
def createJson(fileName, information, outPath):
    if not os.path.isdir(outPath):
        os.makedirs(outPath)
    with open(fileName, 'w') as js:
        json.dump(information, js)
    
def extractQualifications(jobDescription):
    return None 


main()


