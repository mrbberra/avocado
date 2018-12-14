from unittest import TestCase
from selenium import webdriver, common
import json

import flask_server

# run server before running these tests
class ServerTests(TestCase):
    def setUp(self):
        options = webdriver.firefox.options.Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(firefox_options=options)
        self.base_url = 'http://localhost:5000/'

    def test_should_return_json_string_from_data_page(self):
        data_page = self.browser.get(self.base_url + 'data')
        data_elem=self.browser.find_element_by_id('json')
        content=data_elem.text
        json.loads(content) # raises error if not valid json

    def test_should_redirect_unauthorized_admin_access_to_login(self):
        admin_page = self.browser.get(self.base_url + 'admin')
        admin_title = self.browser.find_element_by_tag_name('title')
        self.assertIn('login', self.browser.current_url)

    def tearDown(self):
        self.browser.quit()
