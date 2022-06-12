import nltk
from difflib import SequenceMatcher
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

import warnings
warnings.filterwarnings("ignore")

warnings.filterwarnings("ignore", module='bs4')

def searchBing(query, num):
    url = 'https://www.bing.com/search?q=' + query
    urls = []
    page = requests.get(url, headers = {'User-agent': 'John Doe'})
    soup = bs(page.text, 'html.parser')

    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http'):
            if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
                urls.append(url)
    
    return urls[:num]

def extractText(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return soup.get_text()

#nltk.download('stopwords')
#nltk.download('punkt')
 

def purifyText(string):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = nltk.word_tokenize(string)
    return (" ".join([word for word in words if word not in stop_words]))

def webVerify(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    for url in searchBing(query=string, num=results_per_sentence):
        matching_sites.append(url)
    for sentence in sentences:
        for url in searchBing(query = sentence, num = results_per_sentence):
            matching_sites.append(url)

    return (list(set(matching_sites)))

def similarity(str1, str2):
    #check str1 in str2
    c = 0
    st = str1.split()
    for s in st:
        if s in str2:
            c += 1
    #return (c/len(st))*100
    return (SequenceMatcher(None,str2,str1).ratio())*100

def report(text):

    matching_sites = webVerify(purifyText(text), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(text, extractText(matching_sites[i]))

    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    return matches


def returnTable(dictionary):

    df = pd.DataFrame({'Similarity (%)': dictionary})
    #df = df.fillna(' ').T
    #df = df.transpose()
    return df.to_html()
    
def get_global_score(essay):
    scores = ''
    res = report(essay)
    i = 0
    for k,v in res.items():
        if i > 5: break
        scores += ('\n' + str(k) + ' : ' + str(v))
        i += 1
    return scores

if __name__ == '__main__':
    res = report('''Google began in January 1996 as a research project by Larry Page and Sergey Brin when they were both PhD students at Stanford University in California.[22][23][24] The project initially involved an unofficial "third founder", Scott Hassan, the original lead programmer who wrote much of the code for the original Google Search engine, but he left before Google was officially founded as a company;[25][26] Hassan went on to pursue a career in robotics and founded the company Willow Garage in 2006.''')
    i = 0
    for k,v in res.items():
        if i > 5: break
        print('\n', k, ' : ', v)
        i += 1
