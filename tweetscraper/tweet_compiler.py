from tinydb import TinyDB, Query
import os

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

    def store_historical_tweets():
        historical_fetcher = TweetFetcher().scroll_to_end_of_feed()
        map(lambda tweet_html:
            TweetReader(tweet_html).create_tweet_object().write_to_db(self.db),
            historical_fetcher.get_tweets())

    def get_recent_tweets():
        fetcher = TweetFetcher()
        while True:
            recent_tweets = fetcher.get_tweets() # this scrolls down and loads more each time
            loaded_tweets = map(lambda tweet_html:
                TweetReader(tweet_html).create_tweet_object().write_to_db(self.db),
                recent_tweets)
            new_tweets = filter(lambda tweet:
                not self.db.contains(self.dbQuery['id'] == tweet.id),
                loaded_tweets)
            map(lambda tweet: tweet.write_to_db(self.db), new_tweets)
            if len(new_tweets) < len(loaded_tweets):
                break
            else:
                continue
