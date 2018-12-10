import time
from selenium import webdriver, common
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher

class Tweet:
    def __init__(self, id, timestamp=0, price=-1, location='UK', embed_link=''):
        self.id = id
        self.timestamp = timestamp
        self.price = price
        self.location = location
        self.embed_link = embed_link

    def write_to_json(self):
        # # TODO:
        pass
