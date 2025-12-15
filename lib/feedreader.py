import feedparser
import pandas as pd
import json


class FeedReader:

    def __init__(self, url):
        self.__rss_url = url

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
            # call db insert
            print(f)


if __name__ == '__main__':
    fr = FeedReader('https://www.coindesk.com/arc/outboundfeeds/rss/')
    fr.fetch_rss_feed()
