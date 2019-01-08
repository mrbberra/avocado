import time
from selenium import webdriver, common
from datetime import datetime as dt
from tinydb import TinyDB, Query

from webserver import db
from .tweet_fetcher import TweetFetcher

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
        if isinstance(self.timestamp, dt):
            timestamp_int = int((self.timestamp - dt(2000,1,1)).total_seconds())
        else:
            timestamp_int = self.timestamp # allows for default timestamp is 0
        db.upsert({'id': self.id,
            'timestamp_str': self.timestamp.__str__(),
            'timestamp_int': timestamp_int,
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
