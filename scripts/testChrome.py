from selenium import webdriver
from sys import platform
import time


def run():
    """ test selenium & chrome """
    print('Test Selenium & Chrome...')
    try:
        # whereami
        if platform == "win32":
            cdpath = 'C:/WebDriver/bin/chromedriver.exe'
        else:  # OSX and LInux
            cdpath = '/usr/local/bin/chromedriver'
        driver = webdriver.Chrome(executable_path=cdpath)
        # doyourthing
        url = 'http://www.python.org'
        driver.get(url)
        time.sleep(1)
        print('Title: ' + driver.title)
        driver.quit()
    except Exception as e:
        print('Exception: ' + e.args[0])


if __name__ == '__main__':
    run() # prints to console
    # Test selenium & firefox...
    # Title: Welcome to Python.org
