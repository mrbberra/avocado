from unittest import TestCase
from datetime import datetime as dt
import random

from ..tweet_fetcher import TweetFetcher
from ..tweet_reader import TweetReader

historical_fetcher = TweetFetcher()
raw_tweets = historical_fetcher.get_tweets()
test_tweet = raw_tweets[random.randint(0,10)]

def test_can_get_tweet_id():
    tweet_id = TweetReader(test_tweet).get_id()
    assert isinstance(tweet_id, str)
    assert int(tweet_id) >= 0

def test_can_get_tweet_datetime():
    earliest_acceptable = dt(2008,1,1)
    latest_acceptable = dt.now()
    tweet_time = TweetReader(test_tweet).get_publish_datetime()
    assert tweet_time >= earliest_acceptable
    assert tweet_time <= latest_acceptable

def test_can_get_tweet_text():
    tweet_text = TweetReader(test_tweet).get_clean_text_contents()
    assert isinstance(tweet_text, str)

def test_can_get_embed_link():
    embed_code = TweetReader(test_tweet).get_tweet_embed()
    assert isinstance(embed_code, str)

def test_can_get_price():
    price = TweetReader(test_tweet).get_avocado_price()
    assert price >= -1
    assert price <= 10

historical_fetcher.close_browser()
