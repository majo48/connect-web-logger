"""
    This file contains code for querying the connect-web registered account
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
from logger import local_settings, database
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time, os, traceback


class Session:
    """ login to a HTML session, scrape key: value pairs from website and logout """
    MAXTRY = 10

    def __init__(self, login_url, username, password):
        try:
            self._login(login_url, username, password)
            self._get_system_info()
            self._get_boiler_info()
            self._get_heating_info()
            self._get_tank_info()
            self._get_fead_info()
        except Exception as e:
            print(self.now() + ' >>> Error: ' + str(e))
            traceback.print_exc()
        finally:
            self._logout()

    def __get_value_pairs(self, driver, page_id):
        """ get value pairs from the WebDriver object """
        keys = driver.find_elements_by_xpath("//div[@class='key']")
        if page_id == 'System':
            values = driver.find_elements_by_xpath("//div[@class='value']") # proper spelling in html source
        else:
            values = driver.find_elements_by_xpath("//div[@calss='value']")  # BEWARE: typo in html source
        idx = 0
        while idx < len(keys):
            key = keys[idx].text
            value = values[idx].text
            pair = self.__split_value_unit(value)
            value = pair['value']
            tunit = pair['unit']
            page_idx = str(idx+1)
            if len(page_idx) == 1:
                page_idx = '0' + page_idx
            self.infos.append({
                'customer_id': local_settings.customer_id(),
                'timestamp': self.timestamp,
                'page_id': page_id,
                'page_key' : page_id + page_idx,
                'label': key,
                'value': value,
                'tunit': tunit
            })
            idx += 1 # next key

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
        self.timestamp = self.now()
        print(self.timestamp + ' >>> logging in to url: ' + login_url)
        self.infos = []
        # open login page
        if local_settings.logger_visible_GUI():
            self.driver = webdriver.Firefox()
        else: # False = invisible or no GUI available
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(options=options)
        self.driver.get(login_url)
        # wait for response
        count = 1
        while count <= self.MAXTRY:
            input_tags = self.driver.find_elements_by_xpath("//input")
            if len(input_tags) >= 2:
                break
            time.sleep(1)
            count += 1
        else:
            raise Exception('The browser timed out (login), bad connection?')
        #
        input_tags[0].send_keys(username)
        input_tags[1].send_keys(password)
        button_tags = self.driver.find_elements_by_xpath("//button")
        button_tags[0].click()
        # wait for response after login
        count = 1
        while count <= self.MAXTRY:
            url = self.driver.current_url
            if url == local_settings.facility_url():
                break
            time.sleep(1)
            count += 1
        else:
            raise Exception('The browser timed out (first page), bad connection?')
        print(self.now() + ' >>> successfull login')

    def _get_system_info(self):
        """ scrape infos from the facility info site """
        print(self.now() + ' >>> system info')
        self.driver.get(local_settings.facility_info_url())
        # wait for response
        count = 1
        while count <= self.MAXTRY:
            get_tags = self.driver.find_elements_by_tag_name("froeling-facility-detail-container")
            if len(get_tags) == 1:
                break
            time.sleep(1)
            count += 1
        else:
            raise Exception('The browser timed out (facility information page), bad connection?')
        self.__get_value_pairs(self.driver, 'System')

    def _get_boiler_info(self):
        """ scrape infos from the boiler info site """
        print(self.now() + ' >>> boiler info')
        self.driver.get(local_settings.boiler_info_url())
        # wait for response
        count = 1
        while count <= self.MAXTRY:
            get_tags = self.driver.find_elements_by_tag_name("mat-card-title")
            if len(get_tags) == 1:
                element = get_tags[0].text
                if element.startswith('Boiler'):
                    break
            time.sleep(1)
            count += 1
        else:
            raise Exception('The browser timed out (boiler information page), bad connection?')
        self.__get_value_pairs(self.driver, 'Boiler')

    def _get_heating_info(self):
        """ scrape infos from the heating info site """
        print(self.now() + ' >>> heating circuit 01 info')
        self.driver.get(local_settings.heating_info_url())
        # wait for response
        count = 1
        while count <= self.MAXTRY:
            get_tags = self.driver.find_elements_by_tag_name("mat-card-title")
            if len(get_tags) == 1:
                element = get_tags[0].text
                if element.startswith('Heating'):
                    break
            time.sleep(1)
            count += 1
        else:
            raise Exception('The browser timed out (heating information page), bad connection?')
        self.__get_value_pairs(self.driver, 'Heating')

    def _get_tank_info(self):
        """ scrape infos from the tank info site """
        print(self.now() + ' >>> DHW tank 01 info')
        self.driver.get(local_settings.tank_info_url())
        # wait for response
        count = 1
        while count <= self.MAXTRY:
            get_tags = self.driver.find_elements_by_tag_name("mat-card-title")
            if len(get_tags) == 1:
                element = get_tags[0].text
                if element.startswith('DHW'):
                    break
            time.sleep(1)
            count += 1
        else:
            raise Exception('The browser timed out (DWH tank information page), bad connection?')
        self.__get_value_pairs(self.driver, 'Tank')

    def _get_fead_info(self):
        """ scrape infos from the feed info site """
        print(self.now() + ' >>> feed system info')
        self.driver.get(local_settings.feed_info_url())
        # wait for response
        count = 1
        while count <= self.MAXTRY:
            get_tags = self.driver.find_elements_by_tag_name("mat-card-title")
            if len(get_tags) == 1:
                element = get_tags[0].text
                if element.startswith('Feed'):
                    break
            time.sleep(1)
            count += 1
        else:
            raise Exception('The browser timed out (Feed information page), bad connection?')
        self.__get_value_pairs(self.driver, 'Feed')

    def _logout(self):
        """ logout from the connect-web.froeling.com site """
        print(self.now() + ' >>> logout')
        self.driver.quit()
        # persist data to SQLite database
        db = database.Database()
        for info in self.infos:
            db.insert_log(info)

    def now(self):
        """ get current time as string """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

