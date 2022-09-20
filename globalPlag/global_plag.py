import nltk
import requests
from bs4 import BeautifulSoup as bs
import time
import warnings
#ours:
import search_google
import compare

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
    # i = 0
    # for k,v in res.items():
        # if i > 5: break
        # scores += ('\n' + str(k) + ': ' + str(v))
        # i += 1
    return res

if __name__ == '__main__':
    tic = time.time()
    print(time.ctime())
    # https://www.essaybanyan.com/essay/essay-on-blockchain/
    # https://en.wikipedia.org/wiki/Google
    q = '''Blockchain in simple terms is regarded as the record-keeping technology and has been popular after the advent of Bitcoin. The information regarding different transactions and details of credit and debit are noted down by us and are termed as records. This is the procedure of maintaining the records manually and the manual records are stated as the ledger. The process of maintaining the record of information and data in form of databases that are stored electronically on the computer system is called Blockchain. It can also be regarded as a digital ledger.
        Blockchain technology innovation is proliferating in the hedge fund industry. Blockchain technology plays a primary role in front office and investment functions, in the securing of crypto assets, but also in private investment fund managers’ attempts to satisfy the growth expectations of clients. Although the use of blockchain technology in private investment fund strategies is still in its infancy, as it evolves and accelerates, the associated innovation benefits promise lasting change for the industry.
        Google LLC is an American multinational technology company that focuses on search engine technology, online advertising, cloud computing, computer software, quantum computing, e-commerce, artificial intelligence, and consumer electronics. It has been referred to as the "most powerful company in the world"[10] and one of the world's most valuable brands due to its market dominance, data collection, and technological advantages in the area of artificial intelligence.'''
    res = report(q)
    # i = 0
    # for k,v in res.items():
        # if i > 5: break
        # print(k, ': ', v)
        # i += 1
    tic = time.time() - tic
    i = 1
    for k, v in res.items():
        # print('\n', 'Lines', i, '&', i+1, 'Link:', v,)
        print('\nLines:', i, 'and', i+1, 'Link: ', v[0],' % match:', (round(v[1], 2)))
        i += 2
    print('\ntime: ', tic)
    
