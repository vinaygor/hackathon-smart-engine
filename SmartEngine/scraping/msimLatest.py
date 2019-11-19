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
tileContainer = soup.findAll('a', {"class": "pressCenterLink insightsIndexList"})
print("Len of tile container",len(tileContainer))

tilesAbstract=[]
#for tiles in tileContainer:
    #tiles.find('div',{"class" : "tileText"})
   # tilesAbstract.append((tiles.find('a',{"class" : "tileText"})).text)

articleNames = []
articleLinks = []

for tile in tileContainer:
    articleLinkVal = tile.text
    import re
    articleNameVal = re.sub('[^0-9a-zA-Z]+', '', articleLinkVal)
    articleNames.append(articleNameVal)
    #articleNames.append(tile.text.replace("\'", '').replace("\"", '').replace(' ', '').replace('-', '').replace(',', '').replace('?', '').replace(':', '').replace('.', ''))
    if(".pdf" in tile['href']):
        print("PDF :"+tile['href'])
    else:
        articleLinks.append("https://www.morganstanley.com" + tile['href'])

print(articleNames)
# for articleLink in articleLinks:
#     print("\n",articleLink)


# Create a file for each link
#articleLinks=[]
#articleLinks.append("https://www.morganstanley.com/im/en-us/institutional-investor/insights/macro-insights/australia-housing-bubble-starting-to-deflate.html")
for index, link in enumerate(articleLinks):

   # title = codecs.open(os.path.join(msimFolder,'title.txt'),"w+","utf-8")
   # abstract = codecs.open(os.path.join(msimFolder,'abstract.txt'),'w+',"utf-8")
   # introPara = codecs.open(os.path.join(msimFolder,'introPara.txt'),'w+',"utf-8")
    # print(link)
    html1 = urlopen(link).read()
    # print(html1)
    soup1 = BeautifulSoup(html1)
    # print(soup1)
   # content = soup1.find('div', {"class": "pageDivider"})

   # introParaText = soup1.find('p',{"class" : 'introCallout"'})
   # row = content.find('div', {"class": "row"})

    #data = row.findAll('div')[0]
    # print(content)
    # text = content.findAll('div', {"class": "col-xs-12"})[0]
    # body = text.find('div', {"id": "div_content"})
    # print(body.text)
    import re
   # dataVal = re.sub('[^0-9a-zA-Z]+', ' ', data.text)
    #file.write(dataVal)
  #  dataVal = re.sub('[^0-9a-zA-Z]+', ' ', contentTitle.text)
  #  title.write(contentTitle.text)
    #dataVal = re.sub('[^0-9a-zA-Z]+', ' ', tilesAbstract[index])
    #abstract.write(dataVal)
   # try:
     #   dataVal = re.sub('[^0-9a-zA-Z]+', ' ', introParaText.text)
     #   introPara.write(dataVal)
  #  except:
   #     print("No Intro available")
    try:
        content = soup1.find('div', {"class": "pageDivider"})
        row = content.find('div', {"class": "row"})
        data = row.findAll('div')[0]
        import codecs

        msimFolder = os.path.join(webDirectory, 'MSIM')
        folder = os.makedirs(msimFolder, exist_ok=True)
        FileNameVal = re.sub('[^0-9a-zA-Z]+', '', link)
        fileName = FileNameVal+".txt"
        file = codecs.open(os.path.join(msimFolder, fileName), 'w+', "utf-8")
        contentText = data.text
        import re

        contentTextVal = re.sub('[^0-9a-zA-Z.%$]+', ' ', contentText)
        file.write(contentTextVal)
        file.close()
        print(link,"=====================================================================\n")
        print(fileName, "File Name=====================================================================")
    except:
        print("\n",link)
   # title.close()
   # abstract.close()
  #  introPara.close()

