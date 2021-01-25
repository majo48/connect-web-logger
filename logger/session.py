"""
    This file contains code for querying the connect-web registered account
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)

    This module uses the Google Chrome webdriver, Firefox (geckodriver) is rather buggy and slow.
    Follow the instructions provided in https://sites.google.com/a/chromium.org/chromedriver/home
    The current implementation in MacBook is /usr/local/bin/chromedriver --version
    ChromeDriver 87.0.4280.88 (89e2380a3e36c3464b5dd1302349b1382549290d-refs/branch-heads/4280@{#1761})

"""
from shared import database, local_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sys import platform
import time
import os
import sys
import traceback


class Session:
    """ login to a HTML session, scrape key: value pairs from website and logout """
    MAXTRY = 10

    def __init__(self, login_url, username, password, printer):
        """ initialize a scraping session with connect-web """
        self._success = False
        self.printer = printer
        self.units = { 'percent': '%', 'degrees': '°C', 'hours': 'h', 'tons': 't', 'kilograms': 'kg' }
        try:
            success = self._login(login_url, username, password)
            if success:
                success = self._get_system_info()
            if success:
                success = self._get_boiler_info()
            if success:
                success = self._get_heating_info()
            if success:
                success = self._get_tank_info()
            if success:
                success = self._get_fead_info()
            self._success = success
            self._logout()
            if success:
                # persist infos to SQLite database
                db = database.Database(self.printer)
                for page in self.pages:
                    for info in page:
                        db.insert_log(info)
        #
        except Exception as exc:
            """ manage all and any exceptions in class logger """
            ecxtype = type(exc).__name__
            printer.print(self.now() + ' >>> Error(' + ecxtype + '), ' + str(exc))
            etype, value, tb = sys.exc_info()
            printer.print(''.join(traceback.format_exception(etype, value, tb)))
        finally:
            pass

    def is_successfull(self):
        """ True if the session (login .. logout) was successfull """
        return self._success

    def __wait_for_component(self, component_name):
        """ wait-check for component_name response """
        count = 1
        while count <= self.MAXTRY:
            time.sleep(1) # delayed for dynamic page
            get_component_tags = self.driver.find_elements_by_tag_name("mat-card-title")
            if len(get_component_tags) == 1:
                element = get_component_tags[0].text
                if element.startswith(component_name):
                    break
            self.printer.print(self.now() + ' >>> Retry in wait for component')
            count += 1
        else:
            self.printer.print(self.now() + ' >>> Error: time out in wait for component ' + component_name)
            return False # failed
        return True # success

    def __scroll2bottom(self, driver):
        """
            Scroll to bottom of page:
            1. We need this for small screens (e.g. Windows PC)
            2. dynamic pages need to update the last part of the key, value arrays
            3. else we get unreachable elements with is_displayed() == False
        """
        keys = driver.find_elements_by_xpath("//div[@class='key']")
        target = keys[-1] # last element in array
        driver.execute_script('arguments[0].scrollIntoView(true);', target)
        time.sleep(1)

    def __get_value_pairs(self, driver, page_id):
        """
            get key, value pairs from the WebDriver object
            delay and retry, if any key or value aren't loaded yet (len()==0)
        """
        self.__scroll2bottom(self.driver)
        count = 1
        while count <= self.MAXTRY:
            keys = driver.find_elements_by_xpath("//div[@class='key']")
            if page_id == 'System':
                values = driver.find_elements_by_xpath("//div[@class='value']")  # proper spelling in html source
            else:
                values = driver.find_elements_by_xpath("//div[@calss='value']")  # BEWARE: typo in html source
            pairs, noblanks = self.__join_pairs(keys, values, page_id)
            if noblanks and len(pairs) > 0:
                return pairs # success
            else:
                time.sleep(1)  # delayed retry
                self.printer.print(self.now() + ' >>> Retry in get value pairs for ' + page_id)
                count += 1
        self.printer.print(self.now() + ' >>> Error: time out in get value pairs for ' + page_id)
        return [] # failed

    def __join_pairs(self, keys, values, page_id):
        """ join keys, values and units in a list of tuples """
        pairs = []
        if len(keys) != len(values):
            self.printer.print(self.now() + ' >>> key, value arrays not same length.')
            noblanks = False
            return noblanks, pairs
        noblanks = True
        idx = 0
        while idx < len(keys):
            key = keys[idx].text
            value = values[idx].text
            if len(key) == 0 or len(value) == 0:
                noblanks = False
                break
            pair = self.__split_value_unit(value)
            value = pair['value']
            tunit = pair['unit']
            page_idx = str(idx+1)
            if len(page_idx) == 1:
                page_idx = '0' + page_idx
            pairs.append({
                'customer_id': local_settings.customer_id(),
                'timestamp': self.timestamp,
                'page_id': page_id,
                'page_key' : page_id + page_idx,
                'label': key,
                'value': value,
                'tunit': tunit
            })
            idx += 1 # next key, value
        return pairs, noblanks

    def __split_value_unit(self, value_unit):
        """ properly split values and technical units """
        spos = value_unit.rfind(' ')
        if spos != -1:
            # may contain a technical unit
            u = value_unit[spos+1:]
            v = value_unit[:spos]
            if u in self.units.values():
                return { 'value': v, 'unit': u}
        return {'value': value_unit, 'unit': ''}

    def _login(self, login_url, username, password):
        """ login to the connect-web.froeling.com site """
        self.timestamp = self.now()
        self.printer.print(self.now() + ' >>> login in to url: ' + login_url)
        self.pages = []
        # platform dependent part
        xtime = time.time()
        options = Options()
        if platform == "win32": # Windows 10
            cdpath = 'C:/WebDriver/bin/chromedriver.exe'
            options.headless = False
        elif platform == "darwin":  # OSX High Sierra
            cdpath = '/usr/local/bin/chromedriver'
            options.headless = False
        elif platform == 'linux': # Ubuntu 20.04
            cdpath = '/usr/local/bin/chromedriver'
            options.headless = True
        else:
            raise Exception('Operating system('+platform+') not supported.')
        # start webdriver service
        self.driver = webdriver.Chrome(executable_path=cdpath, options=options)
        self.printer.print(self.now() + ' >>> started webdriver in ' + str(round(time.time() - xtime, 3)) + 'secs.' )
        # open login page
        xtime = time.time()
        self.driver.get(login_url)
        self.printer.print(self.now() + ' >>> loaded login page in ' + str(round(time.time() - xtime, 3)) + 'secs.')
        time.sleep(4) # do absolutely nothing for the first 5 seconds
        # wait-check for response
        count = 1
        while count <= self.MAXTRY:
            time.sleep(1)
            input_tags = self.driver.find_elements_by_tag_name("input")
            button_tags = self.driver.find_elements_by_tag_name("button")
            if len(input_tags) >= 2 and len(button_tags) >= 1:
                break # success
            count += 1
            self.printer.print(self.now() + ' >>> Retry in login page')
        else:
            self.printer.print(self.now() + ' >>> Error: The browser timed out (login) in ' + login_url)
            return False # failed
        # fill out login form
        input_tags[0].send_keys(username)
        input_tags[1].send_keys(password)
        button_tags[0].click()
        # wait-check for response after login
        count = 1
        while count <= self.MAXTRY:
            time.sleep(1)
            url = self.driver.current_url
            if url == local_settings.facility_url():
                break # success
            count += 1
            self.printer.print(self.now() + ' >>> Retry in facility page.')
        else:
            self.printer.print(self.now() + ' >>> Error: The browser timed out (facility page).')
            return False # failed
        return True # success

    def _get_system_info(self):
        """ scrape infos from the facility info site """
        self.printer.print(self.now() + ' >>> system info')
        self.driver.get(local_settings.facility_info_url())
        # wait for response
        count = 1
        while count <= self.MAXTRY:
            time.sleep(1)
            get_tags = self.driver.find_elements_by_tag_name("froeling-facility-detail-container")
            if len(get_tags) == 1:
                break
            count += 1
            self.printer.print(self.now() + ' >>> Retry in system info page.')
        else:
            self.printer.print(self.now() + ' >>> Error: The browser timed out (system info page).')
            return False # failed
        pairs = self.__get_value_pairs(self.driver, 'System')
        self.pages.append(pairs)
        return len(pairs) != 0

    def _get_boiler_info(self):
        """ scrape infos from the components->boiler info site """
        self.printer.print(self.now() + ' >>> boiler info')
        self.driver.get(local_settings.boiler_info_url())
        success = self.__wait_for_component('Boiler')
        if success:
            pairs = self.__get_value_pairs(self.driver, 'Boiler')
            self.pages.append(pairs)
            success = len(pairs) != 0
        return success

    def _get_heating_info(self):
        """ scrape infos from the components->heating info site """
        self.printer.print(self.now() + ' >>> heating circuit 01 info')
        self.driver.get(local_settings.heating_info_url())
        success = self.__wait_for_component('Heating')
        if success:
            pairs = self.__get_value_pairs(self.driver, 'Heating')
            self.pages.append(pairs)
            success = len(pairs) != 0
        return success

    def _get_tank_info(self):
        """ scrape infos from the components->tank info site """
        self.printer.print(self.now() + ' >>> DHW tank 01 info')
        self.driver.get(local_settings.tank_info_url())
        success = self.__wait_for_component('DHW')
        if success:
            pairs = self.__get_value_pairs(self.driver, 'Tank')
            self.pages.append(pairs)
            success = len(pairs) != 0
        return success

    def _get_fead_info(self):
        """ scrape infos from the components->feed info site """
        self.printer.print(self.now() + ' >>> feed system info')
        self.driver.get(local_settings.feed_info_url())
        success = self.__wait_for_component('Feed')
        if success:
            pairs = self.__get_value_pairs(self.driver, 'Feed')
            self.pages.append(pairs)
            success = len(pairs) != 0
        return success

    def _logout(self):
        """ logout from the connect-web.froeling.com site """
        self.printer.print(self.now() + ' >>> logout')
        self.driver.quit()

    def now(self):
        """ get current time as string """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

