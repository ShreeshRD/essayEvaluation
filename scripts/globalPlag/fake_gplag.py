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
    lines = 2 # change how many lines you want checked at a time
    for i in range(0, len(txt_sent), lines):
        j = 0
        sent = ""
        while (i + j) < len(txt_sent):
            sent += txt_sent[i + j] + ' '
            j += 1
            if j >= lines:
                break
        sites = search_google.scrape_google(sent, 5)
        matches = ('', 0)
        for i in range(len(sites)):
            extracted = extract_text(sites[i])
            if extracted:
                temp = compare.sim_score(sent, extracted) * 100
                if temp > matches[1]:
                    matches = (sites[i], temp)
        res[sent] = matches
    return res
    

def get_global_score(essay):
    scores = ''
    res = report(essay)
    i = 0
    for k,v in res.items():
        if v[1] > 30:
            scores += (str(k) + '--> '+ str(round(v[1],1)) + '% match with: <a style="text-decoration: underline;" class="display-5" href=' + str(v[0])  + '>link<a/></br>')
        i += 1
    return scores

if __name__ == '__main__':
    tic = time.time()
    print(time.ctime())
    q = '''Dear local newspaper, I think effects computers have on people are great learning skills/affects because they give us time to chat with friends/new people, helps us learn about the globe(astronomy) and keeps us out of troble! Thing about! Dont you think so? How would you feel if your teenager is always on the phone with friends! Do you ever time to chat with your friends or buisness partner about things. Well now - there's a new way to chat the computer, theirs plenty of sites on the internet to do so: @ORGANIZATION1, @ORGANIZATION2, @CAPS1, facebook, myspace ect. Just think now while your setting up meeting with your boss on the computer, your teenager is having fun on the phone not rushing to get off cause you want to use it. How did you learn about other countrys/states outside of yours? Well I have by computer/internet, it's a new way to learn about what going on in our time! You might think your child spends a lot of time on the computer, but ask them so question about the economy, sea floor spreading or even about the @DATE1's you'll be surprise at how much he/she knows. Believe it or not the computer is much interesting then in class all day reading out of books. If your child is home on your computer or at a local library, it's better than being out with friends being fresh, or being perpressured to doing something they know isnt right. You might not know where your child is, @CAPS2 forbidde in a hospital bed because of a drive-by. Rather than your child on the computer learning, chatting or just playing games, safe and sound in your home or community place. Now I hope you have reached a point to understand and agree with me, because computers can have great effects on you or child because it gives us time to chat with friends/new people, helps us learn about the globe and believe or not keeps us out of troble. Thank you for listening.
'''
    res = report(q)
    tic = time.time() - tic
    for k, v in res.items():
        print(k, v, '\n')
    print('\ntime: ', tic)