import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from googlesearch import search
import time

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query, num):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 'https://google.', 'https://webcache.googleusercontent.', 'http://webcache.googleusercontent.',        'https://policies.google.', 'https://support.google.', 'https://maps.google.', 'https:/youtube.com')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links[:num]

def search_google(query, num):
    return [link for link in search(query, tld='co.in', stop = num)]

if __name__ == '__main__':
    time.sleep(1)
    q = '''Google LLC is an American multinational technology company that focuses on search engine technology, online advertising, cloud computing, computer software, quantum computing, e-commerce, artificial intelligence, and consumer electronics. It has been referred to as the "most powerful company in the world"[10] and one of the world's most valuable brands due to its market dominance, data collection, and technological advantages in the area of artificial intelligence. '''
    for link in scrape_google(q, 2):
        print(link)