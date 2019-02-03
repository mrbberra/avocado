import time
import os
from selenium import webdriver, common

CHROME_BIN = os.environ.get('GOOGLE_CHROME_SHIM')
CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')

class TweetFetcher:
    def __init__(self):
        # load twitter page using selenium
        options = webdriver.chrome.options.Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size=1000x1000')
        options.headless = True
        if CHROMEDRIVER_PATH: # For heroku deploy only
            options.binary_location = CHROME_BIN
            self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                chrome_options=options)
        else:
            self.browser = webdriver.Chrome(options=options)
        self.browser.get('https://twitter.com/hpavocadoprice')

    def _find_timeline_end_div(self):
        max_wait_time = 5
        wait_interval = 0.25
        end_wait_time = time.time() + max_wait_time
        while True:
            try:
                end_div = self.browser.find_element_by_class_name('timeline-end')
                return end_div
            except (common.exceptions.NoSuchElementException) as e:
                if time.time() > end_wait_time:
                    raise e
                time.sleep(wait_interval)

    def scroll_to_end_of_feed(self):
        end_div = self._find_timeline_end_div()
        while True:
            if 'has-more-items' not in end_div.get_attribute('class'):
                break
            else:
                self.browser.execute_script('arguments[0].scrollIntoView();', end_div)
                end_div = self._find_timeline_end_div()
        return end_div

    def get_tweets(self):
        self._find_timeline_end_div() #ensures we have loaded the page
        return self.browser.find_elements_by_class_name('js-stream-item')

    def close_browser(self):
        self.browser.quit()
