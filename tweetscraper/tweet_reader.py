import time
from selenium import webdriver, common
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher

class TweetReader:
    def __init__(self):
        pass

    def get_id(self, raw_tweet):
        return int(raw_tweet.get_attribute('data-item-id'))

    def get_publish_datetime(self, raw_tweet):
        time_div = raw_tweet.find_element_by_css_selector('a.tweet-timestamp')
        time_string = time_div.get_attribute('title')
        if (time_string[0] != '0') & (time_string[1] == ':'):
            time_string = '0' + time_string
        if time_string[12] == ' ':
            time_string = time_string[:11] + '0' + time_string[11]
        string_format = '%I:%M %p - %d %b %Y'
        return dt.strptime(time_string, string_format)

    def get_all_text_contents(self, raw_tweet):
        main_text_elem = raw_tweet.find_element_by_class_name('TweetTextSize')
        quote_text_elem = raw_tweet.find_element_by_class_name('QuoteTweet-text')
        text_elements = [main_text_elem, quote_text_elem]
        strings_without_links = []
        for elem in text_elements:
            str = elem.get_property('innerHTML')
            if len(str.split('<a href')) > 1:
                for substr in str.split('<a href'):
                    substr = substr.split('>')[-1]
                    strings_without_links += [substr]
            else: strings_without_links += [str]
        return ' '.join(strings_without_links)
