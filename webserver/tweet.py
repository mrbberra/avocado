import time
from selenium import webdriver, common
from datetime import datetime as dt
import logging

from webserver import db
from .tweet_fetcher import TweetFetcher

logger = logging.getLogger(__name__)

class PriceValidationError(Exception):
    def __init__(self):
        self.message = 'This is not a valid price.'

class Tweet(db.Model):

    __tablename__ = 'tweet_table'

    id = db.Column(db.String(64),  nullable=False, unique=True, primary_key=True)
    timestamp_str = db.Column(db.String(128),  nullable=False)
    timestamp_int = db.Column(db.BigInteger,  nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(2), nullable=False)
    embed_link = db.Column(db.Text, nullable=False)

    def __init__(self, id, timestamp, price, location, embed_link):
        self.id = id
        self.timestamp_str = timestamp.__str__() # for human-readable api
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

def tweet_upsert(id, timestamp=0, price=-1, location='UK', embed_link=''):
    db_existing_tweet = Tweet.query.filter_by(id=id).first()
    if not db_existing_tweet:
        logger.info('Did not find tweet with id=%s in DB. Inserting', id)
        new_tweet = Tweet(id, timestamp, price, location, embed_link)
        db.session.add(new_tweet)
        db.session.commit()
    else:
        needs_update = False
        if db_existing_tweet.price != price and new_tweet.price != -1: # don't save over priced tweet with unpriced tweet
            db_existing_tweet.price = price
            needs_update = True
        if db_existing_tweet.location != location:
            db_existing_tweet.location = location
            needs_update = True
        if needs_update:
            logger.info('Found tweet with id=%s in DB. Updating', id)
            db.session.commit()
        if needs_update:
            logger.info('Found tweet with id=%s in DB. No change necessary', id)
