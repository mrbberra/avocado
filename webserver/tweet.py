import time
from selenium import webdriver, common
from datetime import datetime as dt
import logging

from webserver import db
from .tweet_fetcher import TweetFetcher

class PriceValidationError(Exception):
    def __init__(self):
        self.message = 'This is not a valid price.'

class Tweet(db.Model):

    __tablename__ = 'tweet_table'

    id = db.Column(db.BigInteger,  nullable=False, unique=True, primary_key=True)
    timestamp_str = db.Column(db.String(128),  nullable=False)
    timestamp_int = db.Column(db.Integer,  nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(2), nullable=False)
    embed_link = db.Column(db.Text, nullable=False)

    def __init__(self, id, timestamp, price, location, embed_link):
        self.id = id
        self.timestamp_str = timestamp.__str__()
        self.timestamp_int = self.calc_int_timestamp(timestamp)
        self.price = price
        self.location = location
        self.embed_link = embed_link

    def calc_int_timestamp(self, timestamp):
        if isinstance(timestamp, dt):
            return int((timestamp - dt(2000,1,1)).total_seconds())
        else:
            return timestamp # allows for default timestamp is 0

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp_str': self.timestamp_str,
            'timestamp_int': self.timestamp_int,
            'price': self.price,
            'location': self.location,
            'embed_link': self.embed_link
        }

def tweet_save_to_db(id, timestamp=0, price=-1, location='UK', embed_link=''):
    tweet = Tweet(id, timestamp, price, location, embed_link)
    db_existing_tweet = Tweet.query.filter_by(id=id).first()
    if not db_existing_tweet:
        db.session.add(tweet)
        db.session.commit()
    elif db_existing_tweet == tweet:
        return
    else:
        db.session.delete(db_existing_tweet)
        db.session.add(tweet)
        db.session.commit()
