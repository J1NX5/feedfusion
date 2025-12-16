import feedparser
import pandas as pd
import json
# from db import DBManager
from lib.db import DBManager
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

    def _read_sources(self):
        with open("sources.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        feeds = config["feeds"]
        return feeds

    # def test_yaml(self):
    #     print(self.__config)


    def fetch_rss_feed(self):
        count = 0

        count_entrys = 0
        count_exists = 0
        count_inserts = 0
        for q in self.__config:
            count += 1
            print(f'Runde: {count}')
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
                count_entrys += 1
                resp = self.__dbm.check_entry_exist(f.id)
                if resp is not None:
                    count_exists += 1
                else:
                    self.__dbm.insert_feed(f.id, f.title, f.link, f.published, f.author, q['name'], 1)
                    count_inserts += 1
        logging.info(f'Entrys: {count_entrys}, exists: {count_exists}, inserts: {count_inserts}')
            

if __name__ == '__main__':
    fr = FeedReader()
    fr.fetch_rss_feed()
