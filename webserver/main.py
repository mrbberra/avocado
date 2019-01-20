import os
import threading
from flask import Flask, render_template, redirect, url_for, request,\
 session, Blueprint

from webserver import db
import webserver.tweet_compiler as tweet_compiler

main_views = Blueprint('main_views', __name__,
                        template_folder='templates')

@main_views.route("/index")
@main_views.route("/")
def index_view():
    return render_template('base.html')

@main_views.route('/admin', methods=['GET', 'POST'])
def admin_view():
    if not session.get('logged_in', False):
        return redirect(url_for('auth_views.login_view'))
    if request.method == 'POST':
        tweet_compiler.update_tweet_price(
            request.form['tweet_id'],
            float(request.form['price'])
        )
    tweets = tweet_compiler.all_tweets_query_admin()
    return render_template('admin.html', tweets=tweets)
