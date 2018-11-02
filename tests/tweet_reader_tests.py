from unittest import TestCase
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader

class TweetReaderTests(TestCase):
    def setUp(self):
        self.historical_fetcher = TweetFetcher()
        self.raw_tweets = self.historical_fetcher.get_tweets()

    def test_can_get_tweet_id(self):
        tweet_id = TweetReader(self.raw_tweets[0]).get_id()
        self.assertGreaterEqual(tweet_id, 0)

    def test_can_get_tweet_datetime(self):
        earliest_acceptable = dt(2008,1,1)
        latest_acceptable = dt.now()
        tweet_time = TweetReader(self.raw_tweets[0]).get_publish_datetime()
        self.assertGreaterEqual(tweet_time, earliest_acceptable)
        self.assertLessEqual(tweet_time, latest_acceptable)

    def test_can_get_tweet_text(self):
        tweet_text = TweetReader(self.raw_tweets[0]).get_clean_text_contents()
        self.assertTrue(isinstance(tweet_text, str))

    def test_can_get_embed_link(self):
        self.assertEquals(
            type(TweetReader(self.raw_tweets[0]).get_tweet_embed()),
            type('df'))

    def tearDown(self):
        self.historical_fetcher.close_browser()
