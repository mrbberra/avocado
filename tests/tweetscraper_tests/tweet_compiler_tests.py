from unittest import TestCase
from tinydb import TinyDB, Query
import os
import json

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader
from tweetscraper.tweet import Tweet, PriceValidationError
from tweetscraper.tweet_compiler import TweetCompiler

class TweetCompilerTests(TestCase):
    def setUp(self):
        self.compiler = TweetCompiler(testing=True)
        self.dbQuery = Query()

    def test_should_use_test_db(self):
        if os.path.exists('test_db.json'):
            os.remove('test_db.json')
        new_compiler = TweetCompiler()
        self.assertTrue(os.path.exists('develop_db.json'))

    def test_should_store_historical_tweets(self):
        self.compiler.get_historical_tweets()
        self.assertGreater(len(self.compiler.db), 0)

    def test_should_access_all_tweets(self):
        Tweet(10).write_to_db(self.compiler.db)
        Tweet(11).write_to_db(self.compiler.db)
        Tweet(12).write_to_db(self.compiler.db)
        self.assertEquals(len(self.compiler.all_tweets_query()), 3)

    def test_should_access_tweet_by_id(self):
        Tweet(10).write_to_db(self.compiler.db)
        Tweet(11).write_to_db(self.compiler.db)
        Tweet(12).write_to_db(self.compiler.db)
        self.assertEquals(self.compiler.tweet_id_query(10)['id'], 10)

    def tearDown(self):
        self.compiler.db.purge_tables()
        self.compiler.db.close()
