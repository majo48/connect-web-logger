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
            self._get_system_info()
            self._get_boiler_info()
            self._get_heating_info()
            self._get_tank_info()
            self._get_fead_info()
        except Exception as e:
            print('Error: ' + str(e))
        finally:
            self._logout()

    def __get_value_pairs(self, driver, page_id):
        """ get value pairs from the WebDriver object """
        keys = driver.find_elements_by_xpath("//div[@class='key']")
        system_page = page_id == 'System'
        if system_page:
            values = driver.find_elements_by_xpath("//div[@class='value']") # proper spelling in html source
            # first thing: build self.timestamp
            idx = 0
            while idx < len(keys):
                key = keys[idx].text
                if key == 'Last signal at':
                    value = values[idx].text
                    self.timestamp = self.__set_timestamp(value)
                    break
                idx += 1 # next key
        else:
            values = driver.find_elements_by_xpath("//div[@calss='value']")  # BEWARE: typo in html source
        idx = 0
        while idx < len(keys):
            key = keys[idx].text
            value = values[idx].text
            pair = self.__split_value_unit(value)
            value = pair['value']
            tunit = pair['unit']
            self.infos.append({
                'customer_id': local_settings.customer_id(),
                'timestamp': self.timestamp,
                'page_id': page_id,
                'label': key,
                'value': value,
                'tunit': tunit
            })
            idx += 1 # next key

    def __set_timestamp(self, value):
        """ set timestamp to format YYYY-MM-DD HH:MM:SS.SSS (SQLite text format) """
        dot = '.'
        year = value[6:10]
        mon = value[3:5]
        day = value[0:2]
        hour = value[11:13]
        min = value[14:16]
        sec = value[17:19]
        return year + '-' + mon + '-' + day + ' ' + hour + ':' + min + ':' + sec + '.000'

    def __split_value_unit(self, value_unit):
        """ properly split values and technical units """
        units = { 'percent': '%', 'degrees': '°C', 'hours': 'h', 'tons': 't', 'kilograms': 'kg' }
        spos = value_unit.rfind(' ')
        if spos != -1:
            # may contain a technical unit
            u = value_unit[spos+1:]
            v = value_unit[:spos]
            if u in units.values():
                return { 'value': v, 'unit': u}
        return {'value': value_unit, 'unit': ''}

    def _login(self, login_url, username, password):
        """ login to the connect-web.froeling.com site """
        print('logging in to url: ' + login_url)
        self.infos = []
        # open login page
        self.driver = webdriver.Firefox()
        self.driver.get(login_url)
        time.sleep(3) # wait 3 seconds for jscript to complete
        input_tags = self.driver.find_elements_by_xpath("//input")
        input_tags[0].send_keys(username)
        input_tags[1].send_keys(password)
        button_tags = self.driver.find_elements_by_xpath("//button")
        button_tags[0].click()
        time.sleep(3) # wait 3 seconds for jscript to complete
        if self.driver.current_url == local_settings.facility_url():
            print('successfull login')
        else:
            print('Error logging in')

    def _get_system_info(self):
        """ scrape infos from the facility info site """
        print('facility info')
        self.driver.get(local_settings.facility_info_url())
        time.sleep(3) # wait 3 seconds for jscript to complete
        self.__get_value_pairs(self.driver, 'System')

    def _get_boiler_info(self):
        """ scrape infos from the boiler info site """
        print('boiler info')
        self.driver.get(local_settings.boiler_info_url())
        time.sleep(3) # wait 3 seconds for jscript to complete
        self.__get_value_pairs(self.driver, 'Boiler')

    def _get_heating_info(self):
        """ scrape infos from the heating info site """
        print('heating circuit 01 info')
        self.driver.get(local_settings.heating_info_url())
        time.sleep(3) # wait 3 seconds for jscript to complete
        self.__get_value_pairs(self.driver, 'Heating')

    def _get_tank_info(self):
        """ scrape infos from the tank info site """
        print('DHW tank 01 info')
        self.driver.get(local_settings.tank_info_url())
        time.sleep(3) # wait 3 seconds for jscript to complete
        self.__get_value_pairs(self.driver, 'Tank')

    def _get_fead_info(self):
        """ scrape infos from the feed info site """
        print('feed system info')
        self.driver.get(local_settings.feed_info_url())
        time.sleep(3) # wait 3 seconds for jscript to complete
        self.__get_value_pairs(self.driver, 'Feed')

    def _logout(self):
        """ logout from the connect-web.froeling.com site """
        print('logout')
        self.driver.quit()
        for info in self.infos:
            print(str(info))


