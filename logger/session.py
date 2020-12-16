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
import time


class Session:
    """ login to a HTML session, scrape key: value pairs from website and logout """
    def __init__(self, login_url, username, password):
        try:
            self._login(login_url, username, password)
            self._get_infos()
        except Exception as e:
            print('Error: ' + str(e))
        finally:
            self._logout()

    def _login(self, login_url, username, password):
        """ login to the connect-web.froeling.com site """
        print('logging in to url: ' + login_url)
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

    def _get_infos(self):
        """ scrape infos from the connect-web.froeling.com site """
        self._get_facility_info()
        self._get_boiler_info()
        self._get_heating_info()
        self._get_tank_info()
        self._get_fead_info()

    def _get_facility_info(self):
        """ scrape infos from the facility info site """
        print('facility info')
        self.driver.get(local_settings.facility_info_url())
        time.sleep(3)
        # wait 3 seconds for jscript to complete
        keys = self.driver.find_elements_by_xpath("//div[@class='key']")
        values = self.driver.find_elements_by_xpath("//div[@class='value']")
        idx = 0
        while idx < len(keys):
            key = keys[idx].text
            value = values[idx].text
            value = value.replace(' h', '') # remove hours designation (redundant)
            print('System information, ' + key + ', ' + value)
            idx = idx + 1

    def _get_boiler_info(self):
        """ scrape infos from the boiler info site """
        print('boiler info')
        self.driver.get(local_settings.boiler_info_url())
        time.sleep(3)
        # wait 3 seconds for jscript to complete
        keys = self.driver.find_elements_by_xpath("//div[@class='key']")
        values = self.driver.find_elements_by_xpath("//div[@calss='value']") # BEWARE: typo in html source
        idx = 0
        while idx < len(keys):
            key = keys[idx].text
            value = values[idx].text
            value = value.replace(' %', '') # remove percent
            value = value.replace(' °C', '') # remove temperatur
            print('Boiler information, ' + key + ', ' + value)
            idx = idx + 1

    def _get_heating_info(self):
        """ scrape infos from the heating info site """
        print('heating circuit 01 info')
        self.driver.get(local_settings.heating_info_url())
        time.sleep(3)
        # wait 3 seconds for jscript to complete
        keys = self.driver.find_elements_by_xpath("//div[@class='key']")
        values = self.driver.find_elements_by_xpath("//div[@calss='value']") # BEWARE: typo in html source
        idx = 0
        while idx < len(keys):
            key = keys[idx].text
            value = values[idx].text
            value = value.replace(' °C', '') # remove temperature
            print('Heating information, ' + key + ', ' + value)
            idx = idx + 1

    def _get_tank_info(self):
        """ scrape infos from the tank info site """
        print('DHW tank 01 info')
        self.driver.get(local_settings.tank_info_url())
        time.sleep(3)
        # wait 3 seconds for jscript to complete
        keys = self.driver.find_elements_by_xpath("//div[@class='key']")
        values = self.driver.find_elements_by_xpath("//div[@calss='value']") # BEWARE: typo in html source
        idx = 0
        while idx < len(keys):
            key = keys[idx].text
            value = values[idx].text
            value = value.replace(' °C', '') # remove temperature
            value = value.replace(' %', '')  # remove percent
            print('Heating information, ' + key + ', ' + value)
            idx = idx + 1
        dummy = 'stop'

    def _get_fead_info(self):
        """ scrape infos from the feed info site """
        print('feed system info')
        pass # work in progress

    def _logout(self):
        """ logout from the connect-web.froeling.com site """
        print('logout')
        self.driver.quit()

