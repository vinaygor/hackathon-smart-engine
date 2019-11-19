#!/usr/bin/env python3
import sys
import os
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
from urllib.request import urlopen
from bs4 import BeautifulSoup
webDirectory = "WEB"
# https://www.privatebank.bankofamerica.com/insights.html?filter=investment-management
html = urlopen("https://www.privatebank.bankofamerica.com/insights.html?filter=investment-management").read()
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
# Result Items Container
articles = soup.findAll('div', {"class": "tile--article-small"})

articleLinks = []
articleNames = []
for article in articles:
    articleLinks.append("https://www.privatebank.bankofamerica.com" + article.find('a')['href'])
    articleNames.append((article.find('a')["aria-label"]).replace("\'", '').replace("\"", '').replace(' ', '').replace('-', '').replace(',', '').replace('?', '').replace(':', '').replace('.', ''))


# print(articleNames)
# print(articleLinks)

# Create a file for each link
for index, link in enumerate(articleLinks):
    boaFolder = os.path.join(webDirectory, 'BOA', articleNames[index])
    folder = os.makedirs(boaFolder, exist_ok=True)
    file = open(os.path.join(boaFolder, 'content.txt'), 'w+')
    fileTitle = open(os.path.join(boaFolder, 'title.txt'), 'w+')
    # print(link)
    html1 = urlopen(link).read()
    # print(html1)
    soup1 = BeautifulSoup(html1)
    # print(soup1)
    contentTitle = soup1.find('h1',{"class" : "article__heading"})
    content = soup1.find('div', {"class": "article__body-content"})
    # print(content)
    # text = content.findAll('div', {"class": "col-xs-12"})[0]
    # body = text.find('div', {"id": "div_content"})
    # print(body.text)
    try:
        import re

        articleNameVal = re.sub('[^0-9a-zA-Z]+', ' ', content.text)
        file.write(articleNameVal)
        cont = "There is a mounting premium on reducing the global footprint of plastic. Countries, companies and consumers are increasingly aware of the plastic plague, putting into motion various efforts on multiple fronts. At the forefront are the following: 1) finding alternative materials to plastics; 2) greater spending on the global recycling infrastructure; 3) increased investment in potential bio-degradable plastic materials; 4) new consumer packaging/wrapping technologies; and 5) a laser-like focus on the creation of the circular economy, where the world of “take, use and dispose” is upended for one that is “reduce, reuse, recycle.” Finally, from the point of view of impact investing, we believe investors could likely reward firms that are at the forefront of finding solutions to the great global plastics crisis."
        contVal = re.sub('[^0-9a-zA-Z]+', ' ', cont)
        fileTitle.write(contVal)
    except:
        print("Error while writing content. ")
    file.close()
    fileTitle.close()
    print("=====================================================================")
