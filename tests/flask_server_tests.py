from unittest import TestCase
from selenium import webdriver, common
import json

from flask_server import FlaskServer

class ServerTests(TestCase):
    def setUp(self):
        self.server = FlaskServer()
        options = webdriver.firefox.options.Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(firefox_options=options)
        self.base_url = 'http://localhost:5000/'

    def test_should_return_json_string(self):
        prices_json = self.browser.get(self.base_url + 'prices.json')
        json.loads(prices_json) # raises error if not valid json

    def tearDown(self):
        self.browser.quit()
        self.server.quit()
