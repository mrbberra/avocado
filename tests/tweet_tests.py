from unittest import TestCase
from tinydb import TinyDB, Query
import os

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader
from tweetscraper.tweet import Tweet, PriceValidationError

class TweetTests(TestCase):
    def setUp(self):
        self.db = TinyDB('testdb.json')
        self.dbQuery = Query()

    def test_should_validate_price(self):
        with self.assertRaises(PriceValidationError):
            tweet = Tweet(id=1, price=43)
            tweet = Tweet(id=1, price='abc1')

    def test_should_write_to_db(self):
        tweet = Tweet(id=1)
        tweet.write_to_db(self.db)
        self.assertTrue(self.db.contains(self.dbQuery.id == 1))

    def test_should_update_db_if_exists(self):
        tweet = Tweet(id=1)
        tweet.write_to_db(self.db)
        tweet.set_price(2)
        tweet.write_to_db(self.db)
        self.assertEquals(self.db.get(self.dbQuery.id == 1)['price'], 2)

    def test_should_not_insert_duplicate_ids(self):
        tweet1 = Tweet(id=1)
        tweet1.write_to_db(self.db)
        tweet2 = Tweet(id=1, price=1)
        tweet2.write_to_db(self.db)
        self.assertEquals(len(self.db.search(self.dbQuery.id == 1)), 1)

    def tearDown(self):
        self.db.close()
        if os.path.exists('testdb.json'):
            os.remove('testdb.json')
