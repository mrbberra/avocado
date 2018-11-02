from unittest import TestCase
from datetime import datetime as dt
import random

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader
from tweetscraper.tweet import Tweet

class TweetReaderTests(TestCase):
    def setUp(self):
        self.historical_fetcher = TweetFetcher()
        raw_tweets = self.historical_fetcher.get_tweets()
        self.test_tweet = raw_tweets[random.randint(0,10)]

    def test_can_get_tweet_id(self):
        tweet_id = TweetReader(self.test_tweet).get_id()
        self.assertGreaterEqual(tweet_id, 0)

    def test_can_get_tweet_datetime(self):
        earliest_acceptable = dt(2008,1,1)
        latest_acceptable = dt.now()
        tweet_time = TweetReader(self.test_tweet).get_publish_datetime()
        self.assertGreaterEqual(tweet_time, earliest_acceptable)
        self.assertLessEqual(tweet_time, latest_acceptable)

    def test_can_get_tweet_text(self):
        tweet_text = TweetReader(self.test_tweet).get_clean_text_contents()
        self.assertTrue(isinstance(tweet_text, str))

    def test_can_get_embed_link(self):
        embed_code = TweetReader(self.test_tweet).get_tweet_embed()
        self.assertEquals(type(embed_code), type('df'))

    def test_can_get_price(self):
        price = TweetReader(self.test_tweet).get_avocado_price()
        self.assertGreaterEqual(price, -1)
        self.assertLessEqual(price, 10)

    def test_can_create_tweet_object(self):
        new_tweet = TweetReader(self.test_tweet).create_tweet_object()
        tweet_exp = Tweet(id=1)
        self.assertEquals(type(new_tweet), type(tweet_exp))

    def tearDown(self):
        self.historical_fetcher.close_browser()
