from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def run():
    """ test selenium & chrome """
    print('Test Selenium & Chrom...')
    url = 'http://www.python.org'
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)
    print('Title: ' + driver.title)
    driver.quit()


if __name__ == '__main__':
    run() # prints to console
    # Test selenium & firefox...
    # Title: Welcome to Python.org
