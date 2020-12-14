""" this file contains code for querying the connect-web registered account
    functions:
        _login(...)
        _get_infos()
        _logout()
"""
from logger import local_settings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Session:
    """ login to a HTML session, scrape key: value pairs from website and logout """
    def __init__(self, login_url, username, password):
        try:
            self._login(login_url, username, password)
            self._get_infos()
            self._logout()
            pass
        except Exception as e:
            print('Error: ' + str(e))
            pass
        finally:
            self._logout()

    def _login(self, login_url, username, password):
        print('loging in to url: ' + login_url)
        # open login page
        self.driver = webdriver.Firefox()
        self.driver.get(login_url)
        # wait for manual login to complete
        WebDriverWait(self.driver, 120).until(EC.url_changes(login_url))
        if self.driver.current_url == local_settings.facility_url():
            # successful login
            print('successfull login')
        else:
            print('Error logging in')
        pass

    def _get_facility_info(self):
        print('facility info')
        self.driver.get(local_settings.facility_info_url())
        #todo continue here
        WebDriverWait(self.driver, 120).until(EC.url_changes(local_settings.facility_info_url()))

    def _get_boiler_info(self):
        print('boiler info')

    def _get_heating_info(self):
        print('heating circuit 01 info')

    def _get_tank_info(self):
        print('DHW tank 01 info')

    def _get_fead_info(self):
        print('feed system info')

    def _get_infos(self):
        self._get_facility_info()
        self._get_boiler_info()
        self._get_heating_info()
        self._get_tank_info()
        self._get_fead_info()
        pass

    def _logout(self):
        print('logout')
        self.driver.quit()

