from unittest import TestCase
from tweetscraper.tweet_fetcher import TweetFetcher

class TweetFetcherTests(TestCase):
    def setUp(self):
        pass

    def test_can_scroll_to_end_of_feed(self):
        fetcher = TweetFetcher()
        end_of_feed_class = fetcher.scroll_to_end_of_feed().get_attribute('class')
        self.assertIn('timeline-end', end_of_feed_class)
        self.assertNotIn('has-more-items', end_of_feed_class)

    def test_can_fetch_a_tweet(self):
        pass

    def tearDown(self):
        pass
