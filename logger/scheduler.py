"""
    This file contains code for scheduling querying the connect-web registered account
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
import schedule
import time
from logger import session, local_settings


class Scheduler:
    """ run the periodic querying of connect-web.froeling.com """

    def __init__(self, username, password, period_minutes):
        """ initialize class, run forever """
        minutes = {
            "15": ["00", "15", "30", "45"],
            "30": ["00", "30"],
            "60": ["00"]
        }
        hours = [
            "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23"
        ]
        # create jobs
        self.jobtimes = []
        for hour in hours:
            for minute in minutes[period_minutes]:
                self.jobtimes.append( hour + ':' + minute )
        # setup job schedules
        for jobtime in self.jobtimes:
            schedule.every().day.at(jobtime).do(self.job, jobtime, username, password)
        # run job schedules
        print(self.now() + ' >>> run jobs scheduled '+str(self.jobtimes))
        while 1:
            schedule.run_pending()
            time.sleep(1)

    def now(self):
        """ get current time as string """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def job(self, jobtime, username, password):
        """ query the connect-web.froeling.com pages once """
        print( self.now() + ' >>> run job ' + jobtime )
        job_session = session.Session(local_settings.login_url(), username, password)
        del job_session

