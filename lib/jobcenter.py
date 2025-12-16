from apscheduler.schedulers.background import BackgroundScheduler
from lib.feedreader import FeedReader
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

class Jobcenter:

    def __init__(self):
        self.__scheduler = BackgroundScheduler()
        # self.scheduler.add_job(self._start_scraper, 'interval', minutes=1)
        logging.info("Get feeds at programm start")
        self._get_feeds()
        self.__scheduler.add_job(self._get_feeds, 'interval', minutes=10)

    def start(self) -> None:
        self.__scheduler.start()
        return logging.info("Jobcenter hat geöffnet")
        

    def _get_feeds(self) -> None:
        logging.info('Start to getting feeds')
        fro = FeedReader()
        fro.fetch_rss_feed()

    
