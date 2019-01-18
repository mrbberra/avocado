# Run a test server.
from webserver import app, tweet_compiler
import threading
import os

if os.environ['DEBUG']:
    DEBUG = True
FLASK_PORT = int(os.environ['PORT'])

tweets = tweet_compiler.TweetCompiler()

live_tweet_thread = threading.Thread(
    name='live-tweet-daemon',
    target=tweets.get_live_tweets,
    kwargs={'timeout':5000}
)
flask_thread = threading.Thread(
    name='flask-app',
    target=app.run,
    kwargs={'debug':DEBUG,'use_reloader':False}
)

flask_thread.start()
tweets.get_historical_tweets()
live_tweet_thread.setDaemon(True)
live_tweet_thread.start()
