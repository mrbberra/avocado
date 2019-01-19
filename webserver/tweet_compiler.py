import os
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',
                    )

from webserver import db
from .tweet_fetcher import TweetFetcher
from .tweet_reader import TweetReader
from .tweet import Tweet

class TweetCompiler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.disable(logging.DEBUG)

    def store_historical_tweets(self):
        historical_fetcher = TweetFetcher()
        self.logger.info('Scrolling to end of feed...')
        historical_fetcher.scroll_to_end_of_feed()
        self.logger.info('Accessing tweets...')
        tweets = historical_fetcher.get_tweets()
        self.logger.info('Parsing and saving tweets...')
        processed_tweets = list(map(lambda tweet_raw:
            TweetReader(tweet_raw).create_and_save_tweet(),
            tweets))
        historical_fetcher.close_browser()

    def get_historical_tweets(self):
        self.logger.info('Fetching historical tweets.')
        if len(Tweet.query.all()) == 0:
            self.store_historical_tweets()
        self.logger.info('Finished fetching historical tweets.')

    def store_recent_tweets(self):
        live_fetcher = TweetFetcher()
        while True:
            self.logger.info('Checking last stored tweet...')
            max_timestamp = db.session.query(db.func.max(Tweet.timestamp_int)).scalar()
            most_recent_tweet = Tweet.query.filter_by(
                timestamp_int=max_timestamp).first()
            if most_recent_tweet_id:
                most_recent_tweet_id = most_recent_tweet.id
            else:
                most_recent_tweet_id = 0
            self.logger.info('Last stored tweet id is %d', most_recent_tweet_id)
            self.logger.info('Fetching a page of tweets...')
            recent_tweets = live_fetcher.get_tweets() # this scrolls down and loads more each time
            self.logger.info('Parsing and saving tweets...')
            loaded_tweet_objects = map(lambda tweet_raw:
                TweetReader(tweet_raw).create_and_save_tweet(),
                recent_tweets)
            self.logger.info('Checking if more tweets need to be loaded...')
            matches_last_stored = list(filter(lambda id:
                id == most_recent_tweet_id,
                loaded_tweet_objects
            ))
            if len(matches_last_stored) > 0:
                self.logger.info('No more tweets to be loaded.')
                break
            else:
                self.logger.info('More tweets need to be loaded.')
                continue
        live_fetcher.close_browser()

    def get_live_tweets(self, timeout):
        while True:
            self.store_recent_tweets()
            time.sleep(timeout)

def all_tweets_query_api():
    tweets = Tweet.query.all()
    tweets = map(lambda x: {
        'id': x.id,
        'timestamp': x.timestamp_str,
        'price': x.price},
        tweets)
    return list(tweets)

def all_tweets_query_admin():
    tweets = Tweet.query.all()
    tweets = map(lambda x: [x.id, x.embed_link, x.price],
        tweets)
    return list(tweets)

def update_tweet_price(id, price):
    round(price, 2)
    tweet = Tweet.query.get(id)
    tweet.price = price
    db.session.commit()
    return

def tweet_id_query(id):
    return Tweet.query.get(id).to_dict()
