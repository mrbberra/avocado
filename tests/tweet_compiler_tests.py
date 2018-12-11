from unittest import TestCase
from tinydb import TinyDB, Query
import os

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader
from tweetscraper.tweet import Tweet, PriceValidationError
from tweetscraper.tweet_compiler import TweetCompiler

class TweetCompilerTests(TestCase):
    def setUp(self):
        self.compiler = TweetCompiler()
        self.dbQuery = Query()

    def test_should_use_dev_db(self):
        if os.path.exists('develop_db.json'):
            os.remove('develop_db.json')
        new_compiler = TweetCompiler()
        self.assertTrue(os.path.exists('develop_db.json'))

    def tearDown(self):
        self.compiler.db.purge_tables()
        self.compiler.db.close()
