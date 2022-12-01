import nltk
import requests
from bs4 import BeautifulSoup as bs
from . import compare
import time
import warnings
from . import search_google

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", module='bs4')

def extract_text(url):
    try:
        page = requests.get(url, timeout=15)
        soup = bs(page.text, 'html.parser')
        res = soup.get_text()
    except:
        res = None
    return res

def report(text):
    res = {}
    txt_sent = nltk.sent_tokenize(text)
    for i in range(0, len(txt_sent), 2):
        sent = txt_sent[i] + ' ' + txt_sent[i+1]
        sites = search_google.scrape_google(sent, 5)
        matches = ('', 0)
        for i in range(len(sites)):
            extracted = extract_text(sites[i])
            if extracted:
                temp = compare.sim_score(sent, extracted) * 100
                if temp > matches[1]:
                    matches = (sites[i], temp)
        # matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
        res[sent] = matches #list(matches.items())[0]
    return res
    

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
    print(time.ctime())
    q = '''In a small saucepan, add finely chopped dark chocolate and a splash of cocoa powder. Stir occasionally until melted. While waiting for that to melt, mix together cornstarch with a small splash of whole milk.  Once chocolate is melted, add the rest of your milk slowly while constantly whisking. Continue to heat until all of it is nice and hot. Then whisk in the cornstarch slurry. Continue to heat until thickened. Pour into a mug, topped with whipped cream and dust with cocoa powder. '''
    res = report(q)
    # i = 0
    # for k,v in res.items():
        # if i > 5: break
        # print(k, ': ', v)
        # i += 1
    tic = time.time() - tic
    for k, v in res.items():
        print(k, v, '\n')
    print('\ntime: ', tic)