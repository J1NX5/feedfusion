import feedparser
import pandas as pd
# import requests
import json
from scraper import FeedScraper


class FeedReader:

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
        # print(f'{fetch_data.keys()}\n {fetch_data}')
        self.get_feed_text(fetch_data.link[0])


        # build json structure and by the field text call get_feed_text func

    # scraper not finish
    def get_feed_text(self, url):
        print(url)
        fso = FeedScraper(url)
        # text = fso.scrape()
        print(fso.scrape())
        # return text

if __name__ == '__main__':
    fr = FeedReader()
    fr.fetch_rss_feed()
