import time
from selenium import webdriver, common
from datetime import datetime as dt
from tinydb import TinyDB, Query

from tweetscraper.tweet_fetcher import TweetFetcher

class PriceValidationError(Exception):
    def __init__(self):
        self.message = 'This is not a valid price.'

class Tweet:
    def __init__(self, id, timestamp=0, price=-1, location='UK', embed_link=''):
        self.id = id
        self.timestamp = timestamp
        self.price = -1
        self.location = location
        self.embed_link = embed_link
        self.set_price(price)

    def write_to_db(self, db):
        dbQuery = Query()
        db.upsert({'id': self.id,
            'timestamp': self.timestamp,
            'price': self.price,
            'location': self.location,
            'embed_link': self.embed_link,
        }, dbQuery.id == self.id)

    def set_price(self, price):
        try:
            price = float(price)
        except ValueError:
            raise PriceValidationError
        if price >= 10:
            raise PriceValidationError
        if price <= 0 and price != -1:
            raise PriceValidationError
        price = round(price, 2)
        self.price = price
