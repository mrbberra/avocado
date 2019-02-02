import pytest
import json

# run server before running these tests
base_url = 'https://avocado-prices.herokuapp.com/'

def test_should_return_json_string_from_data_page(selenium):
    data_page = selenium.get(base_url + 'data')
    data_elem = selenium.find_element_by_id('json')
    content = data_elem.text
    json.loads(content) # raises error if not valid json

def test_should_redirect_unauthorized_admin_access_to_login(selenium):
    admin_page = selenium.get(base_url + 'admin')
    admin_title = selenium.find_element_by_tag_name('title')
    assert 'login' in selenium.current_url
