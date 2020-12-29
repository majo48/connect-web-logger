from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


def run():
    """ test selenium & firefox """
    print('Test selenium & firefox...')
    url = 'http://www.python.org'
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(1)
    print('Title: ' + driver.title)


if __name__ == '__main__':
    run() # prints to console
    # Test selenium & firefox...
    # Title: Welcome to Python.org

