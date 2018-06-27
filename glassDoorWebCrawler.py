#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 13:53:08 2018

@author: victorzhang
"""

import json
import urllib.error, urllib.request, urllib.parse
from bs4 import BeautifulSoup


def harvest(url):
    #access glassdoor website
    print (url)
    req = urllib.request.Request(url, headers={'User-Agent' : "Lennin's Browser"})
    #get html files
    html = urllib.request.urlopen( req ).read()
    #make a soup
    soup = BeautifulSoup(html, "html.parser")
    #get links to jobs (dict obj)
    dictList = json.loads (soup.find('script', type = 'application/ld+json').text  )['itemListElement']
    links = [obj['url'] for obj in dictList]
    #next page
    nextPage = 'https://www.glassdoor.com' + soup.find('li', attrs = {'class': 'next'}).find('a', href = True)['href']
    return links, nextPage
def main():
    print ('Welcome to victors\'s glassdoor web crawling service')
    url =   input ('website address -')
    num = input ('how many pages do you want to search - ')
    myLinks = []
    for counter in range (int(num )):
        links, nextPage = harvest(url)
        url = nextPage
        myLinks += links
    
    print (myLinks)
    
main()
