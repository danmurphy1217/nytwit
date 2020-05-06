import pandas as pd 
import requests
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

"""
@TO DO:
1. load dataframe
2. clean dataframe, get rid of rows with url == "not found"
3. make list of these urls
4. create function which accepts list of urls, goes to that url, gets the body text, tokenizes it by sentence, 
5. adds that tokenized sentence list from [1:-1] to a master list, 
6. joins that master list by string.join(list)
7. adds this cleaned story to a list that will store all stories separated by a comma
8. save this functions output to a var called stories
9. save the content of stories with pickle
10. run funciton

"""

raw_df = pd.DataFrame(pd.read_csv("nytwit_v1-1.tsv", "\t"))
_ = raw_df.loc[raw_df['URL'] == 'not found'] # 189, 243, 277, 278, 290
clean_df = raw_df.drop([189, 243, 277, 278, 290])
url_list = [url for url in clean_df['URL'].values]

def textFromHTML(listOfURLS):
    stories_nytimes = []
    for i, url in enumerate(listOfURLS):
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        textToParse = soup.getText()
        sentence_tokenize = nltk.sent_tokenize(textToParse)
        stories_nytimes.append("".join(sentence_tokenize[1:-1]).replace('\n', ' '))
        print(i)
    return stories_nytimes

x = textFromHTML(url_list)


fname = "stories"
file_saver = open(fname, 'wb')
pickle.dump(x, file_saver)
file_saver.close()

file_loader = open(fname, 'rb')
nytimes_stories_final = pickle.load(file_loader)
file_loader.close()
print('\n')
print(len(nytimes_stories_final))
