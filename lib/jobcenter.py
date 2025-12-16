from apscheduler.schedulers.background import BackgroundScheduler
from lib.feedreader import FeedReader
from lib.database import DBManager
import logging
import time
from newspaper import Article

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
        logging.info("Wait 5 sec.")
        time.sleep(5)
        self._scrape_feed_text()
        self.__scheduler.add_job(self._get_feeds, 'interval', minutes=10)
        self.__scheduler.add_job(self._scrape_feed_text, 'interval', minutes=5)

    def start(self) -> None:
        self.__scheduler.start()
        return logging.info("Jobcenter hat geöffnet")
        

    def _get_feeds(self) -> None:
        logging.info('Run _get_feeds() from jobcenter')
        fro = FeedReader()
        fro.fetch_rss_feed()

    def _scrape_feed_text(self):
        dmo = DBManager()

        # Get 10 of datasets without text and active
        datasets = dmo.get_active_urls_without_text()

        # Iterate dataset
        for d in datasets:
            # 4 is the field with the url -> give it to the scraper
            # print(d[4])
            # fso = FeedScraper(d[4])
            try:
                # html_text = fso.scrape()
                feed_article = Article(d[4])
                feed_article.download()
                feed_article.parse()
                dmo.update_feed_text_by_url(feed_article.text, d[4])
            except Exception as e:
                logging.warning(f'Error: {e}')
        return logging.info("Success running: _scrape_feed_text()")
            


    
