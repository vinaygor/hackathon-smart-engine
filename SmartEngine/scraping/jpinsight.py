#!/usr/bin/env python3
import sys
import os

from operator import abs
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Point:
    articleNames = []
    abstractArticles = []


html = urlopen("https://am.jpmorgan.com/us/en/asset-management/gim/adv/insights/economic-overview").read()
soup = BeautifulSoup(html,"html.parser")
tableContainer = soup.find(id= "Economic&MarketUpdate:Usingthe<em>GuidetotheMarkets</em>toexplaintheinvestmentenvironment")

tableRows = tableContainer.findAll('div', {"class": "fifty"})
dictionaryTitle = {}
dictionaryPara = {}

for index,articleRow in enumerate(tableRows):
    tiles = articleRow.findAll('div', {"class": "basic-text module"})
    for tile in tiles:
        temp = tile.find('h2')
        if temp:
            Point.articleNames.append(temp.text)
            dictionaryTitle = {
                index: temp.text.replace("\"","").replace("\'","").replace(" ","").replace(",","").replace(":","").replace(".","")
            }
        abstracts = tile.findAll('div', {"class": "supporting-copy"})
        for abstract in abstracts:
            image = abstract.find('p', {"class": "slideImg"})
            if not image:


                Point.abstractArticles.append(abstract.text.encode("utf-8"))
                dictionaryPara = {
                    index: abstract.text
                    }

    for(k,v) , (k2,v2) in zip(frozenset(dictionaryTitle.items()), frozenset(dictionaryPara.items())):
        jpFolder = os.path.join("WEB", "JP", str(dictionaryTitle[k]))

        folder = os.makedirs(jpFolder, exist_ok=True)
        file = open(os.path.join(jpFolder, 'content.txt'), 'w+')



        body = str(dictionaryPara[k2])
        file.write(body)
        file.close()

