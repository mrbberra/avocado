import time
from selenium import webdriver, common
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher

class Tweet:
    def __init__(self, id, timestamp=0, price=-1, location='UK', embed_link=''):
        self.id = id
        self.timestamp = timestamp
        self.avocado_price = price
        self.avocado_location = location
        self.embed_link = embed_link

    def write_to_db(self):
        # # TODO:
        pass

    def load_from_db(self):
        # # TODO:
        pass
