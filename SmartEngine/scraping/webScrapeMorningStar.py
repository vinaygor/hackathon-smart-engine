#!/usr/bin/env python3
import sys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

scrapingDirectory = "WEB"
html = urlopen("https://morningstar.in/library/archives.aspx").read()
soup = BeautifulSoup(html)
tableContainer = soup.find('div', {"summary": "An archive of articles"})
table = tableContainer.findAll('div', {"class": "clearfix"})

tableRows = table[0].findAll('div', {"class": "row"})

linkToArticles = []
for articleRow in tableRows:
	linkToArticles.append(articleRow.find('div', {"class" : "col-xs-12"}))

articleLinks = []
for articleLink in linkToArticles:
	articleLinks.append("https://morningstar.in" + articleLink.find('a')['href'])

articleNames = []
for articleLink in linkToArticles:
    articleLinkVal = articleLink.find('a').text
    import re
    articleNameVal = re.sub('[^0-9a-zA-Z]+', '',articleLinkVal)
    articleNames.append(articleNameVal)
	#articleNames.append(articleLink.find('a').text.replace("\'", '').replace("\"", '').replace(' ', '').replace('-','').replace(',','').replace('?','').replace(':','')).replace('$','')

print(articleNames[0])


for index,link in enumerate(articleLinks):
	morningStarFoler = os.path.join(scrapingDirectory,'MSTAR', articleNames[index])
	folder = os.makedirs(morningStarFoler , exist_ok=True)
	file = open(os.path.join(morningStarFoler, 'content.txt'), 'w+')
	html1 = urlopen(link).read()
	soup1 = BeautifulSoup(html1)
	content = soup1.find('div', {"class": "contentpagewrap"})
	text = content.findAll('div', {"class": "col-xs-12"})[0]
	body = text.find('div', {"id": "div_content"})
	#print(body.text)
	try:
		file.write(body.text)
	except:
		print("An exception occurred for article: ",articleNames[index])
	file.close()
	print("=====================================================================")
