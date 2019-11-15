#!/usr/bin/env python3
import sys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
webDirectory = "WEB"
# https://www.investmentbank.barclays.com/our-insights.html
html = urlopen("https://www.mckinsey.com/industries/financial-services/our-insights/corporate-and-investment-banking").read()
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
# Result Items Container
resultContainer = soup.find('section', {"data-module": "InsightsFactory"})
# print(resultContainer)
# Insights container
insightsContainer = resultContainer.find('div', {"class": "block-list"})
# print(insightsContainer)
# all insights

insights = insightsContainer.findAll('div', {"class": "item"})
# print(len(insights))

articleNames = []
articleLinks = []
for insight in insights:
    articleLinks.append("https://www.mckinsey.com" + insight.find('a', {"class": "item-title-link"})['href'])
    articleNames.append((insight.find('a', {"class": "item-title-link"})).find('h3').text.replace("\'", '').replace("\"", '').replace(' ', '').replace('-','').replace(',','').replace('?','').replace(':',''))

# print(articleLinks)
# print(articleNames)

# Create a file for each link
for index, link in enumerate(articleLinks):
    mckinseyFolder = os.path.join(webDirectory, 'MCKISNEY', articleNames[index])
    folder = os.makedirs(mckinseyFolder, exist_ok=True)
    file = open(os.path.join(mckinseyFolder, 'content.txt'), 'w+')
    # print(link)
    html1 = urlopen(link).read()
    # print(html1)
    soup1 = BeautifulSoup(html1)
    # print(soup1)
    content = soup1.find('div', {"class": "text-longform"})
    if content == None:
        content = soup1.find('article', {"class": "text-longform"})
    # print(content)
    # text = content.findAll('div', {"class": "col-xs-12"})[0]
    # body = text.find('div', {"id": "div_content"})
    # print(body.text)
    file.write(content.text)
    file.close()
    print("=====================================================================")

