import time
from selenium import webdriver, common
from datetime import datetime as dt

from tweetscraper.tweet_fetcher import TweetFetcher

class TweetReader:
    def __init__(self, raw_tweet):
        self.raw_tweet = raw_tweet

    def get_id(self):
        return int(self.raw_tweet.get_attribute('data-item-id'))

    def get_publish_datetime(self):
        time_div = self.raw_tweet.find_element_by_css_selector('a.tweet-timestamp')
        time_string = time_div.get_attribute('title')
        if (time_string[0] != '0') & (time_string[1] == ':'):
            time_string = '0' + time_string
        if time_string[12] == ' ':
            time_string = time_string[:11] + '0' + time_string[11:]
        string_format = '%I:%M %p - %d %b %Y'
        return dt.strptime(time_string, string_format)

    def get_clean_text_contents(self):
        main_text = self.raw_tweet\
            .find_element_by_class_name('TweetTextSize')\
            .get_property('innerHTML')
        try:
            quote_text = self.raw_tweet\
                .find_element_by_class_name('QuoteTweet-text')\
                .get_property('innerHTML')
        except (common.exceptions.NoSuchElementException) as e:
            quote_text = ''
        text_elements = [main_text, quote_text]
        full_text_no_links = ''
        for str in text_elements:
            if len(str.split('<a href')) > 1:
                for substr in str.split('<a href'):
                    substr = substr.split('>')[-1]
                    ' '.join([full_text_no_links, substr])
            else: ' '.join([full_text_no_links, str])
        return full_text_no_links

    def get_tweet_embed(self):
        main_text = self.raw_tweet.find_element_by_class_name('TweetTextSize') \
            .get_property('innerHTML')
        time_div = self.raw_tweet.find_element_by_css_selector('a.tweet-timestamp')
        time_string = time_div.get_attribute('title')
        date_str = time_string.split('-')[1].strip()

        embed = '<blockquote class="twitter-tweet" '
        embed += 'data-lang="en"><p lang="en" dir="ltr">'
        embed += main_text
        embed += '</p>&mdash; HP 🥑vocado (@hpavocadoprice) <a href="'
        embed += 'https://twitter.com/hpavocadoprice/status/'
        embed += str(self.get_id())
        embed += '?ref_src=twsrc%5Etfw">'
        embed += date_str
        embed += '</a></blockquote>\n'
        embed += '<script async src="https://platform.twitter.com/widgets.js" '
        embed += 'charset="utf-8"></script>'
        return embed
