import feedparser
import pandas as pd
import requests
import os

url = os.environ.get("URL")
model_name = os.environ.get("MODEL")

def fetch_rss_feed(url):

    raw_feed = feedparser.parse(url)
    data = pd.DataFrame(raw_feed['entries'])
    print(f'{data.keys()}\n {data}')

def ask_ollama(question):
    pass



# Has this keys: 'bozo', 'entries', 'feed', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'
rss_url = "https://www.wallstreet-online.de/rss/nachrichten-aktien-indizes.xml"


if __name__ == '__main__':
    fetch_rss_feed(rss_url)