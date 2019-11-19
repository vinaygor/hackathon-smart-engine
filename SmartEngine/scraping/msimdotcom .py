#!/usr/bin/env python3
import sys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

scrapingDirectory = "WEB"
html = urlopen("https://www.morganstanley.com/im/en-us/financial-advisor/insights.html").read()
soup = BeautifulSoup(html)
tableContainer = soup.find('div', {"id": "latestInsights"})
linkToArticles = tableContainer.findAll('h4', {"class": "media-heading"})

articleLinks = []
articleNames = []
for articleLink in linkToArticles:
	articleLinkVal = articleLink.find('a')['href']
	articleNameText = articleLink.find('a').text
	import re
	articleNameVal = re.sub('[^0-9a-zA-Z]+', '', articleNameText)
	articleNames.append(articleNameVal)
	if not articleLinkVal.endswith(".pdf"):
		articleLinks.append("https://www.morganstanley.com" + articleLink.find('a')['href'])

articleLinks = []
articleLinks.append("https://www.morganstanley.com/im/en-us/financial-advisor/insights/investment-insights/journey-into-the-unknown.html")

for index,link in enumerate(articleLinks):
	html1 = urlopen(link).read()
	soup1 = BeautifulSoup(html1)
	insightsContents = soup1.find('div', {"class": "insightsContent"})
	print("\nLink: ", articleLinks[index])
	for content in insightsContents:
		try:
			text = content.findAll('p')
			msimFolder = os.path.join(scrapingDirectory,'MSIMDOTCOM', articleNames[index])
			folder = os.makedirs(msimFolder , exist_ok=True)
			file = open(os.path.join(msimFolder, 'content.txt'), 'w+')

			#body = text.find('div', {"id": "div_content"})
			body = text
		except:
			print("No Insight content found. Maybe Audio or Video article.")
		#print(body.text)
		try:
			for contentval in body:
				file.write(contentval.text)
		except:
			print("An exception occurred for article: ",articleNames[index])
		file.close()
		print("=====================================================================")
