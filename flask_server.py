from tinydb import TinyDB, Query
import os
from flask import Flask, jsonify
from flask_login import LoginManager, login_required
import threading

from tweetscraper.tweet_compiler import TweetCompiler

app = Flask(__name__)
login = LoginManager(app)

@app.route("/data")
def tweets_data_all():
    return jsonify(tweet_compiler.all_tweets_query())

@app.route('/data/<int:tweet_id>')
def tweets_data_id(tweet_id):
    return jsonify(tweet_compiler.tweet_id_query(tweet_id))

@app.route('/admin')
@login_required
def admin_page():
    return render_template('base.html')

live_tweet_thread = threading.Thread(
    name='live-tweet-daemon',
    target=TweetCompiler().get_live_tweets,
    kwargs={'timeout':5000}
)
flask_thread = threading.Thread(
    name='flask-app',
    target=app.run,
    kwargs={'port':5000,'debug':True,'use_reloader':False}
)

if __name__ == "__main__":
    tweet_compiler = TweetCompiler()
    tweet_compiler.get_historical_tweets()
    live_tweet_thread.setDaemon(True)
    live_tweet_thread.start()
    flask_thread.start()
