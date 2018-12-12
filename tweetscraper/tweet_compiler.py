from tinydb import TinyDB, Query
import os
import time

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader
from tweetscraper.tweet import Tweet

class TweetCompiler:
    def __init__(self):
        if os.environ.get('USE_PROD_DB', False):
            self.db = TinyDB('prod_db.json')
        else:
            self.db = TinyDB('develop_db.json')
        self.dbQuery = Query()

    def store_historical_tweets(self):
        historical_fetcher = TweetFetcher()
        historical_fetcher.scroll_to_end_of_feed()
        tweets = historical_fetcher.get_tweets()
        processed_tweets = list(map(lambda tweet_raw:
            TweetReader(tweet_raw).create_tweet_object(),
            tweets))
        for tweet in processed_tweets:
            tweet.write_to_db(self.db)

    def get_historical_tweets(self):
        if len(self.db) == 0:
            self.store_historical_tweets()

    def store_recent_tweets(self):
        fetcher = TweetFetcher()
        while True:
            recent_tweets = fetcher.get_tweets() # this scrolls down and loads more each time
            loaded_tweets = map(lambda tweet_raw:
                TweetReader(tweet_raw).create_tweet_object().write_to_db(self.db),
                recent_tweets)
            new_tweets = list(filter(lambda tweet:
                not self.db.contains(self.dbQuery['id'] == tweet.id),
                loaded_tweets))
            map(lambda tweet: tweet.write_to_db(self.db), new_tweets)
            if len(new_tweets) < len(loaded_tweets):
                break
            else:
                continue

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
