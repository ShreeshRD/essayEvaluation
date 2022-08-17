import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import urllib
from googlesearch import search
from bs4 import BeautifulSoup as bs

#using this now:
def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query, num):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://policies.google.',
                      'https://support.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links[:num]

#not using:
def search_google(query):
    return [link for link in search(query, tld='co.in', stop = 20)]

def search_bing(query, num):
    url = 'https://www.google.com/search?q=' + query
    urls = []
    page = requests.get(url, headers = {'User-agent': 'John Doe'})
    soup = bs(page.text, 'html.parser')

    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http'):
            if not url.startswith('http://go.m') and not url.startswith('https://go.m') and url not in urls:
                urls.append(url)
    return urls[:num]

if __name__ == '__main__':
    for link in scrape_google("Wikipedia", 10):
        print(link)
