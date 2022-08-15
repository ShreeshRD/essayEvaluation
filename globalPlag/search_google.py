import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

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


if __name__ == '__main__':
    for link in scrape_google("Wikipedia", 10):
        print(link)
