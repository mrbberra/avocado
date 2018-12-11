from unittest import TestCase
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher
from tweetscraper.tweet_reader import TweetReader
from tweet import Tweet

class TweetFetcherTests(TestCase):
    def setUp(self):
        self.historical_fetcher = TweetFetcher()

    def test_can_scroll_to_end_of_feed(self):
        end_of_feed_class = self.historical_fetcher \
            .scroll_to_end_of_feed() \
            .get_attribute('class')
        self.assertIn('timeline-end', end_of_feed_class)
        self.assertNotIn('has-more-items', end_of_feed_class)

    def test_can_and_only_fetches_tweets(self):
        tweets = self.historical_fetcher.get_tweets()
        for tweet in tweets:
            self.assertEqual('tweet', tweet.get_attribute('data-item-type'))

    def tearDown(self):
        self.historical_fetcher.close_browser()
