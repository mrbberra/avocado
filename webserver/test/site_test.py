import pytest
import json
import os
from selenium.webdriver.common.keys import Keys

# run server before running these tests
base_url = 'http://localhost:' + os.environ['PORT'] + '/'
print(base_url)

def test_data_page(selenium):
    # user visits data portal, sees JSON list of all the tweets
    data_page = selenium.get(base_url + 'data')
    data_elem = selenium.find_element_by_css_selector('pre')
    content = data_elem.text
    data = json.loads(content) # raises error if not valid json

    # sees id, price, and integer timestamp for each tweet
    # TODO

def test_login_and_logout(selenium):
    password = os.environ['PASSWORD']
    incorrect_password = 'incorrect_test_pass'

    # user tries to access admin page, is redirected to login
    admin_page_attempt = selenium.get(base_url + 'admin')
    assert 'login' in selenium.current_url

    # user tries to login with incorrect password, is redirected to login
    username_input = selenium.find_element_by_id('username')
    username_input.send_keys('admin')
    password_input = selenium.find_element_by_id('password')
    password_input.send_keys(incorrect_password)
    selenium.find_element_by_xpath("//input[@type='submit']").click()
    assert 'login' in selenium.current_url

    # user logs in with correct password, is redirected to admin page
    username_input = selenium.find_element_by_id('username')
    username_input.send_keys('admin')
    password_input = selenium.find_element_by_id('password')
    password_input.send_keys(password)
    selenium.find_element_by_xpath("//input[@type='submit']").click()
    assert 'admin' in selenium.current_url

    # user visits logout page, logs out and is redirected to login page
    logout_page = selenium.get(base_url + 'logout')
    selenium.find_element_by_xpath("//input[@type='submit']").click()
    assert 'login' in selenium.current_url

    # user tries to access admin page again, is redirected to login
    admin_page_attempt = selenium.get(base_url + 'admin')
    assert 'login' in selenium.current_url

    # user tries to access logout page, is redirected to login
    logout_page_attempt = selenium.get(base_url + 'logout')
    assert 'login' in selenium.current_url
