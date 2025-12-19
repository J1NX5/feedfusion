import feedparser
import pandas as pd
import json
# for lokal testing -> uncomment next line; comment out -> from lib.db import DBManager
from lib.database import DBManager
# from database import DBManager
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
                desired_cols = ['id', 'title', 'tags', 'link', 'published', 'author']
                existing_cols = [c for c in desired_cols if c in pre_data.keys()]
                fetch_data = pre_data[existing_cols]
                for f in fetch_data.itertuples(index=False):
                    if q['name'] == 'coindesk':
                        print(f)
                    count_data[q['name']]['count_feeds'] += 1
                    resp = self.__dbm.check_entry_exist(f.id)
                    if hasattr(f, "tags"):
                        tag_string = self._prepare_tags(f.tags) if f.tags else None
                    else:
                        tag_string = None

                    if hasattr(f, "author"):
                        author = f.author
                    else:
                        author = None

                    if hasattr(f, "published"):
                        published = f.published
                    else:
                        published = None
                    if resp is not None:
                        count_data[q['name']]['count_exists'] += 1
                    else:
                        # if q['name'] == 'CNBC - Earnings':
                        #     print(f.id, q['name'], f.title, tag_string, f.link, f.published, f.author)
                        self.__dbm.insert_feed(f.id, q['name'], f.title, tag_string, f.link, published, author, 1)
                        count_data[q['name']]['count_inserts'] += 1
        except Exception as e:
            logging.info(f'Error {e}')
        return logging.info(count_data)
    
    def _prepare_tags(self,raw_tags):
        rt = raw_tags
        tags_string = ""
        if not isinstance(rt, float):
            for e in rt:
                tags_string += e.term + ", "
        else:
            tags_string = None
        return tags_string

if __name__ == '__main__':
    fr = FeedReader()
    fr.fetch_rss_feed()
