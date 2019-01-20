from flask import Flask, jsonify, Blueprint

from webserver import db
import webserver.tweet_compiler as tweet_compiler

api_views = Blueprint('api_views', __name__)


@api_views.route("/")
def tweets_data_all():
    return jsonify(tweet_compiler.all_tweets_query_api())

@api_views.route('/<tweet_id>')
def tweets_data_id(tweet_id):
    return jsonify(tweet_compiler.tweet_id_query(tweet_id))
