#!/usr/bin/env python3
import sys
import os

from operator import abs
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Point:
    articleNames = []
    abstractArticles = []


html = urlopen("https://am.jpmorgan.com/us/en/asset-management/gim/adv/insights/guide-to-the-markets/quarterly-perspectives").read()
soup = BeautifulSoup(html,"html.parser")
tableContainer = soup.find(id= "LATESTQUARTERLYPERSPECTIVES")


tableRows = tableContainer.findAll('div', {"class": "fifty"})
dictionaryTitle = {}
dictionaryPara = {}

for index,articleRow in enumerate(tableRows):
    tiles = articleRow.findAll('div', {"class": "basic-text module"})
    for tile in tiles:
        abstracts = tile.findAll('div', {"class": "supporting-copy"})
        for abstract in abstracts:
            temp = abstract.find('h5')
            if temp:
                dictionaryTitle = {
                    index: temp.text.replace("\"", "").replace("\'", "").replace(" ", "").replace(",", "").replace(":","").replace(".", "").replace("\r\n","").replace("\t","")
                }
            image = abstract.find('p', {"class": "slideImg"})
            if not image:
                dictionaryPara = {
                    index: abstract.text
                    }

    for(k,v) , (k2,v2) in zip(frozenset(dictionaryTitle.items()), frozenset(dictionaryPara.items())):
        jpFolder = os.path.join('WEB','JP','PortfolioInsights', str(dictionaryTitle[k]))
        folder = os.makedirs(jpFolder, exist_ok=True)
        file = open(os.path.join(jpFolder, 'content.txt'), 'w+')
        body = str(dictionaryPara[k2])
        file.write(body)
        file.close()
