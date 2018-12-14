from tinydb import TinyDB, Query
import os
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',
                    )

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader
from tweetscraper.tweet import Tweet

class TweetCompiler:
    def __init__(self, testing=False):
        if testing == True:
            self.db = TinyDB('test_db.json')
        elif os.environ.get('USE_PROD_DB', False):
            self.db = TinyDB('prod_db.json')
        else:
            self.db = TinyDB('develop_db.json')
        self.dbQuery = Query()
        self.logger = logging.getLogger(__name__)
        logging.disable(logging.DEBUG)

    def store_historical_tweets(self):
        historical_fetcher = TweetFetcher()
        self.logger.info('Scrolling to end of feed...')
        historical_fetcher.scroll_to_end_of_feed()
        self.logger.info('Accessing tweets...')
        tweets = historical_fetcher.get_tweets()
        self.logger.info('Parsing tweets...')
        processed_tweets = list(map(lambda tweet_raw:
            TweetReader(tweet_raw).create_tweet_object(),
            tweets))
        self.logger.info('Saving tweets...')
        for tweet in reversed(processed_tweets):
            tweet.write_to_db(self.db)
        historical_fetcher.close_browser()

    def get_historical_tweets(self):
        self.logger.info('Fetching historical tweets.')
        if len(self.db) == 0:
            self.store_historical_tweets()
        self.logger.info('Finished fetching historical tweets.')

    def store_recent_tweets(self):
        live_fetcher = TweetFetcher()
        while True:
            self.logger.info('Checking last stored tweet...')
            last_stored_tweet = self.db.get(doc_id=len(self.db))
            self.logger.info('Last stored tweet id is %d', last_stored_tweet['id'])
            self.logger.info('Fetching a page of tweets...')
            recent_tweets = live_fetcher.get_tweets() # this scrolls down and loads more each time
            self.logger.info('Parsing tweets...')
            loaded_tweet_objects = map(lambda tweet_raw:
                TweetReader(tweet_raw).create_tweet_object(),
                recent_tweets)
            self.logger.info('Saving tweets...')
            map(lambda tweet: tweet.write_to_db(self.db), loaded_tweet_objects)
            self.logger.info('Checking if more tweets need to be loaded...')
            matches_last_stored = list(filter(lambda tweet:
                last_stored_tweet['id'] == tweet.id,
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

    def all_tweets_query(self):
        tweets = self.db.search(self.dbQuery.id.exists())
        tweets = map(lambda x: {
            'id': x['id'],
            'timestamp': x['timestamp_str'],
            'price': x['price']},
            tweets)
        return list(tweets)

    def tweet_id_query(self, id):
        return self.db.get(self.dbQuery.id == id)
