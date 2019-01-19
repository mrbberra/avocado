# For running just the live tweet fetcher dyno, from the Procfile
from webserver import tweet_compiler

tweets = tweet_compiler.TweetCompiler()
target=tweets.get_live_tweets(timeout=5000)
