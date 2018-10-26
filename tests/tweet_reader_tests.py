from unittest import TestCase
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader

class TweetFetcherTests(TestCase):
    def setUp(self):
        self.historical_fetcher = TweetFetcher()
        self.historical_fetcher.scroll_to_end_of_feed() # make sure page is loaded
        self.raw_tweets = self.historical_fetcher.get_tweets()

    def test_can_get_single_tweet_id(self):
        tweet_id = TweetReader().get_id(self.raw_tweets[0])
        print("id: %d", tweet_id)
        self.assertGreaterEqual(tweet_id, 0)

    def test_can_get_single_tweet_datetime(self):
        earliest_acceptable = dt(2008,1,1)
        latest_acceptable = dt.now()
        tweet_time = TweetReader().get_publish_datetime(self.raw_tweets[0])
        self.assertGreaterEqual(tweet_time, earliest_acceptable)
        self.assertLessEqual(tweet_time, latest_acceptable)

    def test_can_get_tweet_text(self):
        tweet_text = TweetReader().get_all_text_contents(self.raw_tweets[1])
        self.assertTrue(isinstance(tweet_text, str))

    def tearDown(self):
        self.historical_fetcher.close_browser()
