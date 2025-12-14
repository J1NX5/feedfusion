import feedparser
import pandas as pd
import requests

class Feedreader:

    def __init__(self):
        self.__rss_url = "https://www.wallstreet-online.de/rss/nachrichten-aktien-indizes.xml"

    def fetch_rss_feed(self):
        raw_feed = feedparser.parse(self.__rss_url)
        pre_data = pd.DataFrame(raw_feed['entries'])
        fetch_data = pre_data[[
            'title',
            'summary',
            'link',
            'updated'
        ]]
        print(f'{fetch_data.keys()}\n {fetch_data}')


if __name__ == '__main__':
    fr = Feedreader()
    fr.fetch_rss_feed()
