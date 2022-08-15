import nltk
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import compare
import time
import warnings
import search_google

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", module='bs4')

def search_bing(query, num):
    return search_google.scrape_google(query, num)

def extract_text(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return soup.get_text()

def purify_text(string):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = nltk.word_tokenize(string)
    return (" ".join([word for word in words if word not in stop_words]))

def web_verify(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    for url in search_bing(query=string, num=results_per_sentence):
        matching_sites.append(url)
    for sentence in sentences:
        for url in search_bing(query = sentence, num = results_per_sentence):
            matching_sites.append(url)

    return (list(set(matching_sites)))

def similarity(str1, str2):
    return compare.sim_score(str1, str2) * 100

def report(text):

    matching_sites = web_verify(purify_text(text), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(text, extract_text(matching_sites[i]))

    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    return matches

def get_global_score(essay):
    scores = ''
    res = report(essay)
    i = 0
    for k,v in res.items():
        if i > 5: break
        scores += ('\n' + str(k) + ': ' + str(v))
        i += 1
    return scores

if __name__ == '__main__':
    tic = time.time()
    res = report('''Google LLC (/ˈɡuːɡəl/ (listen)) is an American multinational technology company that focuses on search engine technology, online advertising, cloud computing, computer software, quantum computing, e-commerce, artificial intelligence,[9] and consumer electronics. It has been referred to as the "most powerful company in the world"[10] and one of the world's most valuable brands due to its market dominance, data collection, and technological advantages in the area of artificial intelligence.[11][12][13] It is considered one of the Big Five American information technology companies, alongside Amazon, Apple, Meta, and Microsoft.''')
    i = 0
    for k,v in res.items():
        if i > 5: break
        print('\n', k, ': ', v)
        i += 1
    print('time: ', time.time() - tic)
