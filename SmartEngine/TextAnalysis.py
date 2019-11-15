#!/usr/bin/env python3

import os
import sys
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

print("########################## STARTING EXECUTION ##########################")
key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
os.environ[key_var_name] = '5161bb3d82cf4f82ae863db3126a91e6'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
os.environ[endpoint_var_name] = 'https://text-analytics-mkt-1.cognitiveservices.azure.com/'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]


def authenticateClient():
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client


def entity_recognition():
    client = authenticateClient()

    try:
        documents = [
            {"id": "1", "language": "en",
             "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800."},
            {"id": "2", "language": "es",
             "text": "La sede principal de Microsoft se encuentra en la ciudad de Redmond, a 21 kilómetros de Seattle."}
        ]
        response = client.entities(documents=documents)

        for document in response.documents:
            print("Document Id: ", document.id)
            print("\tKey Entities:")
            for entity in document.entities:
                print("\t\t", "NAME: ", entity.name, "\tType: ",
                      entity.type, "\tSub-type: ", entity.sub_type)
                for match in entity.matches:
                    print("\t\t\tOffset: ", match.offset, "\tLength: ", match.length, "\tScore: ",
                          "{:.2f}".format(match.entity_type_score))

    except Exception as err:
        print("Encountered exception. {}".format(err))


def key_phrases(text):
    client = authenticateClient()
    try:
        documents = [
            {"id": "1", "language": "en", "text": text}
        ]

        for document in documents:
            print("Asking key-phrases on '{}' (id: {})".format(document['text'], document['id']))

        response = client.key_phrases(documents=documents)

        phrases = ""
        for document in response.documents:
            phrases = document.key_phrases

        return phrases
    except Exception as err:
        print("Encountered exception. {}".format(err))


def main(webDirectory):
    # entity_recognition()
    print("Main Method !!!")
    files = [];
    print("Scanning Folder : ", webDirectory)
    # r=root, d=directories, f = files
    for r, d, f in os.walk(webDirectory):
        for file in f:
            if 'content.txt' in file:
                files.append(os.path.join(r, file))

    for contentFile in files:
        with open(contentFile, 'r') as f:
            currentDirPath = os.path.dirname(contentFile)
            data = f.read()
            print("Processing file ", contentFile)
            # phrases = "test"
            phrases = key_phrases(data)
            print("Obtained Phrases for file ", contentFile)
            phraseFile = os.path.join(currentDirPath, 'phrases.txt')
            #currentDirPath+"\\phrases.txt"
            with open(phraseFile, 'w') as p:
                try:
                    p.write("\n".join(phrases))
                except:
                    print("Error while writing data to phrases file")

if __name__ == "__main__":
    main()