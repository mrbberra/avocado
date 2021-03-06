# For running all the threads- used for local development in place of Procfile
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
    kwargs={'port':FLASK_PORT,'debug':DEBUG,'use_reloader':False}
)

tweets.get_historical_tweets()
live_tweet_thread.setDaemon(True)
live_tweet_thread.start()
flask_thread.start()
