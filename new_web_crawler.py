#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 19:18:53 2018

@author: victorzhang
"""

import json
import urllib.error, urllib.request, urllib.parse
from bs4 import BeautifulSoup


def kickStarter(url):
    #access glassdoor website
    req = urllib.request.Request(url, headers={'User-Agent' : "Lennin's Browser"})
    #get html files
    html = urllib.request.urlopen(req).read()
    #make a soup
    soup = BeautifulSoup(html, "html.parser")
    #get links to jobs (dict obj)
    dictList = json.loads (soup.find('script', type = 'application/ld+json').text)['itemListElement']
    links = [obj['url'] for obj in dictList]
    return links

def harvest(url):
    print ('********')
    
    req = urllib.request.Request(url, headers={'User-Agent' : "Safari"})
    #get html files
    html = urllib.request.urlopen(req).read()
    #make a soup
    soup = BeautifulSoup(html, 'html.parser')
    #get links to jobs (dict obj)
    dictList = soup.find_all('li', {'class':'jobWrapper'})
    #it should not be empty 
    print (dictList)
    print ('********')
def main():
    print ('Welcome to victors\'s glassdoor web crawling service')
    #url =   input ('website address -')
    #must be the first page appeares in search 
    #an url example
    url = 'https://www.glassdoor.com/Job/los-angeles-data-analytics-intern-jobs-SRCH_IL.0,11_IC1146821_KO12,33.htm?srs=RECENT_SEARCHES'
    myLinks = kickStarter(url)
    for link in myLinks:
        try:
            harvest(link)
        except:
            print ('related job not found')
            print (link)
main()