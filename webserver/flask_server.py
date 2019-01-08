from tinydb import TinyDB, Query
import os
import threading
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify, render_template, redirect, url_for, request,\
 abort, session, flash
from flask_wtf.csrf import CSRFProtect

from tweetscraper import db
from tweetscraper.tweet_compiler import TweetCompiler

csrf = CSRFProtect(app)
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

def validate_login(username, password):
    print(password_hash)
    print(password)
    print(generate_password_hash(password))
    if check_password_hash(ADMIN_PASSWORD_HASH, password) and username == 'admin':
        print('login validated')
        return True
    else:
        return False

#################### VIEWS #####################

@app.route("/data")
def tweets_data_all():
    return jsonify(tweet_compiler.all_tweets_query_api())

@app.route('/data/<int:tweet_id>')
def tweets_data_id(tweet_id):
    return jsonify(tweet_compiler.tweet_id_query(tweet_id))

@app.route("/index")
@app.route("/")
def index_view():
    return render_template('base.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_view():
    if not session.get('logged_in', False):
        return redirect(url_for('login_view'))
    if request.method == 'POST':
        tweet_compiler.update_tweet_price(
            int(request.form['tweet_id']),
            float(request.form['price'])
        )
    tweets = tweet_compiler.all_tweets_query_admin()
    return render_template('admin.html', tweets=tweets)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if session.get('logged_in', False):
        return redirect(url_for('admin_view'))
    if request.method == 'POST':
        if validate_login(request.form['username'],request.form['password']):
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('admin_view'))
        else:
            return render_template('login.html',
                error='Invalid Credentials. Please try again.')
    else:
        return render_template('login.html', error=None)

@app.route('/logout', methods=['GET','POST'])
def logout_view():
    if not session.get('logged_in', False):
        flash('You are already logged out')
        return redirect(url_for('login_view'))
    if request.method == 'POST':
        session['logged_in'] = False
        flash('You were successfully logged out')
        return redirect(url_for('login_view'))
    else:
        return render_template('logout.html', error=None)

if __name__ == "__main__":
    run_app()
