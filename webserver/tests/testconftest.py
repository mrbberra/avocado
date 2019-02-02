import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--live",
                      action="store_true",
                      default=False,
                      help="Run against live site. Defaults to false.")
    parser.addoption("--port",
                      action="store",
                      dest="port",
                      default="5000",
                      help="For use if not using live site. Specifies the port. Defaults to 5000")
    parser.addoption("--browser",
                      action="store",
                      dest="browser",
                      default="firefox",
                      help="Browser. Defaults to firefox, valid options are chrome or firefox")

@pytest.fixture(scope='session')
def base_url():
    if pytest.config.getoption('--live'):
        return 'avocado-prices.herokuapp.com'
    else:
        return 'http://localhost:' + pytest.config.getoption('--port')

@pytest.fixture(scope='session')
def driver(request):
    if pytest.config.getoption('--browser') == 'firefox':
        options = webdriver.firefox.options.Options()
        options.set_headless(headless=True)
        browser = webdriver.Firefox(firefox_options=options)
    else:
        options = webdriver.chrome.options.Options()
        options.set_headless(headless=True)
        browser = webdriver.Chrome(chrome_options=options)
    request.addfinalizer(browser.quit())
    return browser
