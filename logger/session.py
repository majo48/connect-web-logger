""" this file contains code for querying the connect-web registered account
    functions:
        _login
        _get_infos
        _logout
"""

class Session:
    """ open, close a HTML session, scrape key: value pairs from website """
    def __init__(self, login_url, username, password):
        self._login(login_url, username, password)
        self._get_infos()
        self._logout()
        pass


    def _login(self, login_url, username, password):
        print('login to url: '+login_url)


    def _get_facility_info(self):
        print('facility info')


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
