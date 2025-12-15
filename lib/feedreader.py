import feedparser
import pandas as pd
import json
from lib.db import DBManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('log.txt'), 
        logging.StreamHandler()
    ]
)


class FeedReader:

    def __init__(self, url):
        self.__rss_url = url
        self.__dbm = DBManager()

    def fetch_rss_feed(self):
        raw_feed = feedparser.parse(self.__rss_url)
        pre_data = pd.DataFrame(raw_feed.entries)
        fetch_data = pre_data[[
            'id',
            'title',
            'summary',
            'link',
            'published',
            'author'            
        ]]
        for f in fetch_data.itertuples(index=False):
            self.__dbm.insert_feed(f.id, f.title, f.summary, f.link, f.published, f.author)

if __name__ == '__main__':
    fr = FeedReader('https://www.coindesk.com/arc/outboundfeeds/rss/')
    fr.fetch_rss_feed()
