from tinydb import TinyDB, Query
import os
from flask import Flask, jsonify, render_template, redirect, url_for, request, abort
from flask_login import LoginManager, login_user, current_user, login_required
import threading
from login_functions import User, is_safe_url

from tweetscraper.tweet_compiler import TweetCompiler

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login_view'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
tweet_compiler = TweetCompiler()

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

def run_app():
    tweet_compiler = TweetCompiler()
    tweet_compiler.get_historical_tweets()
    live_tweet_thread.setDaemon(True)
    live_tweet_thread.start()
    flask_thread.start()

@login_manager.user_loader
def load_user(user_id):
    return User()

#################### VIEWS #####################

@app.route("/data")
def tweets_data_all():
    return jsonify(tweet_compiler.all_tweets_query())

@app.route('/data/<int:tweet_id>')
def tweets_data_id(tweet_id):
    return jsonify(tweet_compiler.tweet_id_query(tweet_id))

@app.route("/index")
def index_view():
    return render_template('base.html')

@app.route('/admin')
@login_required
def admin_view():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('admin_view'))
    if request.method == 'POST':
        user = User()
        if user.validate(request.form['username'], request.form['password']):
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(url_for('admin_view'))
        else:
            return render_template('login.html',
                error='Invalid Credentials. Please try again.')
    else:
        return render_template('login.html', error=None)

@app.route('/logout', methods=['GET', 'POST'])
def logout_view():
    if not current_user.is_authenticated:
        return redirect(url_for('index_view'))
    if request.method == 'POST':
        user = User()
        user.logout()
        return redirect(url_for('login_view'))
    else:
        return render_template('logout.html', error=None)

if __name__ == "__main__":
    run_app()
