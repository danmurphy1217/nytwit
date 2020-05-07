import pandas as pd
import numpy as np
import requests
import nltk
import pickle
import string
from urllib.request import urlopen
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, listOfUrls, csvFile):
        self.listOfUrls = listOfUrls
        self.csvFile = csvFile

    def nytScraper(self, listOfUrls):
        stories_nytimes = []
        for i, url in enumerate(listOfUrls):

            html = urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            htmlSection = soup.find('section', {
                'name': 'articleBody'
            })
            textToParse = htmlSection.getText()
            sentence_tokenize = nltk.sent_tokenize(textToParse)
            stories_nytimes.append(str("".join(sentence_tokenize[:])).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))))
            print(i)
        return stories_nytimes


class Main:
        raw_df = pd.DataFrame(pd.read_csv("nytwit_v1-1.tsv", sep='\t'))
        clean_df = raw_df.drop(list(raw_df.loc[raw_df['URL'] == 'not found'].index))
        url_list  = [url for url in clean_df['URL'].values]
        x = Scraper(listOfUrls=url_list, csvFile=None)
        pick = x.nytScraper(url_list)
        print(pick)

        fname = "stories"
        file_saver = open(fname, 'wb')
        pickle.dump(pick, file_saver)
        file_saver.close()

        file_loader = open(fname, 'rb')
        nytimes_stories_final = pickle.load(file_loader)
        file_loader.close()
        print('\n')
        df = pd.DataFrame(pd.read_pickle(fname))
        print(df.head(15))

