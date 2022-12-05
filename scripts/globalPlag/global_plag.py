import nltk
import requests
from bs4 import BeautifulSoup as bs
# from . import compare
# import compare, search_google
import time
import warnings
# from . import search_google
import asyncio
from sklearn.feature_extraction.text import HashingVectorizer #, CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

@background
def extract_text(url):
    try:
        page = requests.get(url, timeout=15)
        soup = bs(page.text, 'html.parser')
        res = soup.get_text()
        limit = 5*10**4
        res = " ".join(res.split())
        n = len(res)
        n = min(n, limit)
        res = res[:n]
    except:
        res = ''
    return res

@background
def search(query, num):
    url = 'https://www.bing.com/search?q=' + query
    urls = []
    page = requests.get(url, headers = {'User-agent': 'John Wick'})
    soup = bs(page.text, 'html.parser')

    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http'):
            if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
                urls.append(url)
    # print(urls[:num])
    return '*#-*-#*'.join(urls[:num])

@background
def sim_score(pat, txt,):
    vectorizer = HashingVectorizer()
    txt = txt.lower().split(' ')
    pat = pat.lower().split(' ')
    m = len(pat)
    n = len(txt)
    res = 0
    p_hsh = sum([ord(ch) for ch in ''.join(pat)])
    t_hsh = sum([ord(ch) for ch in ''.join(txt[:m])])
    p_vec = vectorizer.fit_transform([' '.join(pat)]).toarray()
    
    if abs(p_hsh - t_hsh) < 10 * m:
        t_vec = vectorizer.fit_transform([' '.join(txt[:m])]).toarray()
        score = cosine_similarity(p_vec, t_vec)[0][0]
        res = max(res, score)
    
    for i in range(n - m):
        t_hsh -= sum([ord(ch) for ch in txt[i]])
        t_hsh += sum([ord(ch) for ch in txt[i+m]])
        if abs(p_hsh - t_hsh) <= 10 * m:
            t_vec = vectorizer.fit_transform([' '.join(txt[i+1:i + m+1])]).toarray()
            score = cosine_similarity(p_vec, t_vec)[0][0]
            res = max(res, score)
    return round(res*100,2)

def report(text, check_links):
    t = time.time()
    # check_links = 3
    txt_sent = nltk.sent_tokenize(text)
    print('num of sents: ', len(txt_sent))
    
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    looper = asyncio.gather(*[search(sent, check_links) for sent in txt_sent])
    sites = loop.run_until_complete(looper)
    links = []
    for ss in sites:
        links += ss.split('*#-*-#*')
    for i in range(5):
        print(links[i])
    print('num of links: ', len(links))
    print('time till now: ', time.time() - t)
    
    # loop = asyncio.get_event_loop()
    looper = asyncio.gather(*[extract_text(link) for link in links])
    ex_txt = loop.run_until_complete(looper)
    print('num of ex_txt: ', len(ex_txt))
    print('time till now: ', time.time() - t)
    # till here 35 sec
    
    looper = asyncio.gather(*[sim_score(txt_sent[i//check_links], ex_txt[i]) for i in range(len(ex_txt))])
    scores = loop.run_until_complete(looper)
    print('num of scores: ', len(scores))
    print('time till now: ', time.time() - t)
    
    res = {}
    for i in range(0,len(scores), check_links):
        mscore = max(scores[i:i+5])
        idd = scores[i:i+5].index(mscore) + i
        res[txt_sent[i//check_links]] = (links[idd], mscore)
    # print(res)
    return res

def get_global_score(essay, check_links):
    scores = []
    res = report(essay, check_links)
    i = 0
    for k,v in res.items():
        if v[1] >= 50:
            # scores += str(k) + '--> '+ str(round(v[1],1)) + '% match with: <a style="text-decoration: underline;" class="display-5" href=' + str(v[0])  + '>link<a/></br>'
            scores.append([i+1, str(k), str(round(v[1],1)), str(v[0])])
        i += 1
    return scores

if __name__ == '__main__':
    tic = time.time()
    q = '''Dear local  newspaper, I think effects computers have on people are great learning skills/affects because they give us time to chat with friends/new people, helps us learn about the globe(astronomy) and keeps us out of troble! Thing about! Dont you think so? How would you feel if your teenager is always on the phone with friends! Do you ever time to chat with your friends or buisness partner about things. Well now - there's a new way to chat the computer, theirs plenty of sites on the internet to do so: @ORGANIZATION1, @ORGANIZATION2, @CAPS1, facebook, myspace ect. Just think now while your setting up meeting with your boss on the computer, your teenager is having fun on the phone not rushing to get off cause you want to use it. How did you learn about other countrys/states outside of yours? Well I have by computer/internet, it's a new way to learn about what going on in our time! You might think your child spends a lot of time on the computer, but ask them so question about the economy, sea floor spreading or even about the @DATE1's you'll be surprise at how much he/she knows. Believe it or not the computer is much interesting then in class all day reading out of books. If your child is home on your computer or at a local library, it's better than being out with friends being fresh, or being perpressured to doing something they know isnt right. You might not know where your child is, @CAPS2 forbidde in a hospital bed because of a drive-by. Rather than your child on the computer learning, chatting or just playing games, safe and sound in your home or community place. Now I hope you have reached a point to understand and agree with me, because computers can have great effects on you or child because it gives us time to chat with friends/new people, helps us learn about the globe and believe or not keeps us out of troble. Thank you for listening.
'''
    print('Starting now')
    scores = get_global_score(q)
    # scores = report(q)
    print(scores)
    print('total time taken: ', time.time() - tic)
    
