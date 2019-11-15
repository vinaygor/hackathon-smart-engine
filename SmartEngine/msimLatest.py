#!/usr/bin/env python3
import sys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

webDirectory = "WEB"
# https://www.morganstanley.com/im/en-us/institutional-investor/insights.html
html = urlopen("https://www.morganstanley.com/im/en-us/institutional-investor/insights.html").read()
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
# Result Items Container
tileContainer = soup.findAll('div', {"class": "insightArticleTile"})
print("Len of tile container",len(tileContainer))

tilesAbstract=[]
for tiles in tileContainer:
    #tiles.find('div',{"class" : "tileText"})
    tilesAbstract.append((tiles.find('div',{"class" : "tileText"})).text)

articleNames = []
articleLinks = []

for tile in tileContainer:
    articleNames.append(
        (tile.find('div', {"class": "tileTitle"})).text.replace("\'", '').replace("\"", '').replace(' ', '').replace(
            '-', '').replace(',', '').replace('?', '').replace(':', '').replace('.', ''))
    articleLinks.append("https://www.morganstanley.com" + tile.find('a')['href'])

print(articleNames)
print(articleLinks)

# Create a file for each link
for index, link in enumerate(articleLinks):
    import codecs
    msimFolder = os.path.join(webDirectory, 'MSIM', articleNames[index])
    folder = os.makedirs(msimFolder, exist_ok=True)
    file = codecs.open(os.path.join(msimFolder, 'content.txt'), 'w+',"utf-8")
    title = codecs.open(os.path.join(msimFolder,'title.txt'),"w+","utf-8")
    abstract = codecs.open(os.path.join(msimFolder,'abstract.txt'),'w+',"utf-8")
    introPara = codecs.open(os.path.join(msimFolder,'introPara.txt'),'w+',"utf-8")
    # print(link)
    html1 = urlopen(link).read()
    # print(html1)
    soup1 = BeautifulSoup(html1)
    # print(soup1)
    content = soup1.find('div', {"class": "pageDivider"})
    contentTitle = soup1.find('div',{"class" : "heroProductName"})
    introParaText = soup1.find('p',{"class" : 'introCallout"'})
    row = content.find('div', {"class": "row"})

    data = row.findAll('div')[0]
    # print(content)
    # text = content.findAll('div', {"class": "col-xs-12"})[0]
    # body = text.find('div', {"id": "div_content"})
    # print(body.text)
    import re
    dataVal = re.sub('[^0-9a-zA-Z]+', ' ', data.text)
    file.write(dataVal)
    dataVal = re.sub('[^0-9a-zA-Z]+', ' ', contentTitle.text)
    title.write(contentTitle.text)
    dataVal = re.sub('[^0-9a-zA-Z]+', ' ', tilesAbstract[index])
    abstract.write(dataVal)
    try:
        dataVal = re.sub('[^0-9a-zA-Z]+', ' ', introParaText.text)
        introPara.write(dataVal)
    except:
        print("No Intro available")
    file.close()
    title.close()
    abstract.close()
    introPara.close()
    print("=====================================================================")

