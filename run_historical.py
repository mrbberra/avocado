# For running the historical tweet fetcher, generally as a one-off dyno
from webserver import tweet_compiler

tweets = tweet_compiler.TweetCompiler()
target=tweets.get_historical_tweets()
