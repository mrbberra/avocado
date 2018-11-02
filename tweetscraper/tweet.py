import time
from selenium import webdriver, common
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher

class Tweet:
    def __init__(self, id, timestamp, tweet_text,
        avocado_price=-1, avocado_location='UK', embed_link=''):
        self.id = id
        self.timestamp = timestamp
        self.tweet_text = tweet_text
        self.avocado_price = avocado_price
        self.avocado_location = avocado_location
        self.embed_link = embed_link
