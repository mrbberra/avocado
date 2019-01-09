# Run a test server.
from webserver import app, tweet_compiler
import threading

tweets = tweet_compiler.TweetCompiler()

live_tweet_thread = threading.Thread(
    name='live-tweet-daemon',
    target=tweets.get_live_tweets,
    kwargs={'timeout':5000}
)
flask_thread = threading.Thread(
    name='flask-app',
    target=app.run,
    kwargs={'port':5000,'debug':True,'use_reloader':False}
)

tweets.get_historical_tweets()
live_tweet_thread.setDaemon(True)
live_tweet_thread.start()
flask_thread.start()
