from tinydb import TinyDB, Query
import os
from flask import Flask, jsonify
import threading

from tweetscraper.tweet_compiler import TweetCompiler

tweet_compiler = TweetCompiler()
tweet_compiler.get_historical_tweets()
#live_tweet_thread = threading.Thread(
#    target=tweet_compiler.get_live_tweets(3000)
#)
#live_tweet_thread.start()
app = Flask(__name__)

@app.route("/tweets_data/all")
def tweets_data_all():
    return jsonify(tweet_compiler.all_tweets_query())

@app.route('/tweets_data/<int:tweet_id>')
def tweets_data_id(tweet_id):
    return jsonify(tweet_compiler.tweet_id_query(tweet_id))

if __name__ == "__main__":
    app.run(port=5000,debug=True)
