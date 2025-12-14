from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
from datetime import datetime
import json
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

class FeedScraper:

    def __init__(self, url):

        self.__base_url = url

        # date_today for cvs name
        self.__date_today = datetime.today().strftime('%Y-%m-%d')

        # url of chromedriver for docker build
        # self.__service = Service('/usr/local/bin/chromedriver')
        # url of chromedriver for local testing
        self.__service = Service('/usr/bin/chromedriver')

        self.__chrome_options = Options()

        # url of browser for docker build
        # self.__chrome_options.binary_location = '/usr/bin/google-chrome'
        # url of browser for local testing
        self.__chrome_options.binary_location = '/usr/bin/chromium-browser'

        # self.__chrome_options.add_argument("--headless=new")
        self.__chrome_options.add_argument("--no-sandbox")
        self.__chrome_options.add_argument("--disable-dev-shm-usage")
        # self.__chrome_options.add_argument("--headless")
        self.__chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0')
        self.__chrome_options.page_load_strategy = 'eager'
        self.__driver = webdriver.Chrome(service=self.__service, options=self.__chrome_options)

    # def wait(func):
    #     def wrapper(*args, **kwargs):
    #         logging.info("decorator @wait is called")
    #         time.sleep(2)
    #         return func(*args, **kwargs)
    #     return wrapper


    # The decorator is called befor the function is called
    #  @wait
    def scrape(self):
        logging.info("Start function")
        self.__driver.get(self.__base_url)
        self.__driver.execute_script("""
            var buttons = document.querySelectorAll('button');
            for(var btn of buttons) {
                if(btn.textContent.includes('Accept') || btn.textContent.includes('Akzeptieren und weiter')) {
                    btn.click(); break;
                }
            }
        """)
        # page_string = BeautifulSoup(self.__driver.page_source, 'html.parser').find(class_="total")
       
        self.__driver.quit() 
        return logging.info("function is finish and driver has quit")

if __name__ == "__main__":
    fso = FinanceScraper()
    fso.scrape()