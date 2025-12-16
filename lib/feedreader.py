import feedparser
import pandas as pd
import json
# for lokal testing -> uncomment next line; comment out -> from lib.db import DBManager
from lib.database import DBManager
# from lib.db import DBManager
import logging
import yaml

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

    def __init__(self):
        self.__dbm = DBManager()
        self.__config = self._read_sources()
        logging.info('Config are loaded')

    def _read_sources(self):
        with open("sources.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        feeds = config["feeds"]
        return feeds

    # def test_yaml(self):
    #     print(self.__config)

    def fetch_rss_feed(self):
        try:
            count_sources = len(self.__config)
            count_data = {}
            for q in self.__config:
                count_data[q['name']] = {
                    'count_feeds':0,
                    'count_exists':0,
                    'count_inserts':0
                }
                # print(f'Quelle: {q['name']}, Url: {q['url']}')
                '''
                In this run:
                q['name'] is the name of the source for table
                q['url'] is url for the parser
                '''
                raw_feed = feedparser.parse(q['url'])
                pre_data = pd.DataFrame(raw_feed.entries)
                # print(pre_data.keys())
                fetch_data = pre_data[[
                    'id',
                    'title',
                    'link',
                    'published',
                    'author'         
                ]]

                for f in fetch_data.itertuples(index=False):
                    count_data[q['name']]['count_feeds'] += 1
                    resp = self.__dbm.check_entry_exist(f.id)
                    if resp is not None:
                        count_data[q['name']]['count_exists'] += 1
                    else:
                        self.__dbm.insert_feed(f.id, f.title, f.link, f.published, f.author, q['name'], 1)
                        count_data[q['name']]['count_inserts'] += 1
        except Exception as e:
            logging.info(f'Error {e}')
        return logging.info(count_data)       

if __name__ == '__main__':
    fr = FeedReader()
    fr.fetch_rss_feed()
