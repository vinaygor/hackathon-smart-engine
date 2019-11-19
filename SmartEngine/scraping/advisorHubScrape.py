#!/usr/bin/env python3
import sys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

webDirectory = "WEB"

html = urlopen("https://advisorhub.com/news/").read()
soup = BeautifulSoup(html)
mainContent = soup.find('div', {"class": "mainContent"})
postsContainer = mainContent.find('div', {"class": "posts"})

posts = postsContainer.findAll('div', {"class": "post"})

linkToArticles = []
for post in posts[:5]:
    linkToArticles.append(post.find('a')['href'])

# print(linkToArticles)

articleNames = []
for post in posts[:5]:
    articleNames.append(
        (post.find('h2')).find('a').text.replace("\'", "").replace("\"", "").replace(" ", "").replace("-", "").replace(
            ":", "").replace(".", "").replace(",", ""))

# print(articleNames)

# articleLinks = []
# for articleLink in linkToArticles:
#     articleLinks.append("https://advisorhub.com" + articleLink.find('a')['href'])
#
# articleNames = []
# for articleLink in linkToArticles:
#     articleNames.append(
#         articleLink.find('a').text.replace("\'", '').replace("\"", '').replace(' ', '').replace("-", ''))
#
# print(articleNames[0])
#
# # Create a file for each link
#
#
for index, link in enumerate(linkToArticles):
    advisoryHubFolder = os.path.join(webDirectory, 'ADVISORHUB', articleNames[index])
    folder = os.makedirs(advisoryHubFolder, exist_ok=True)
    file = open(os.path.join(advisoryHubFolder, 'content.txt'), 'w+')
    html1 = urlopen(link).read()
    soup1 = BeautifulSoup(html1)
    content = soup1.find('div', {"class": "mainContent"})
    text = content.findAll('div', {"class": "post"})[0]
    # body = text.find('div', {"id": "div_content"})
    # print(body.text)
    file.write(text.text)
    file.close()
    print("=====================================================================")
