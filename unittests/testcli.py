"""
    Testcases for the logger app
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
    functions:
        testRunCLI: test command line interface
"""

import unittest
import io
import os
from contextlib import redirect_stdout
from logger import app as loggerapp
from shared import database
from shared import printlog
from plotter import app as plotterapp


class TestRunCLI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test0database(self):
        """ test if database has enough contents for plotting (2 snapshots) """
        db = database.Database(print())
        cnt = db.count_logs()
        self.assertGreater(cnt, 2 * 47, "Test environment is not clean!")

    def test1RunCliLogger(self):
        """ run scripting part of plotter app """
        db = database.Database(print())
        cnt = db.count_logs()
        if cnt < + 2 * 47:
            self.skipTest("Test environment is not clean!")
        loggerapp.run('unittest')
        my_printer = printlog.PrintLog('testcli.log')
        foldername = my_printer.get_foldername()
        filename = foldername + my_printer.get_slash() + 'logger.log'
        exists = os.path.isfile(filename)
        self.assertTrue(exists, msg='Missing logger.log file!')
        if exists:
            with open(filename) as f:
                errors = 'Error(' in f.read()
                self.assertFalse(errors, msg='Error in logger.log file!')

    def test2RunCliPlotter(self):
        """ run scripting part of plotter app """
        db = database.Database(print())
        cnt = db.count_logs()
        if cnt < + 2 * 47:
            self.skipTest("Test environment is not clean!")
        plotterapp.run()
        my_printer = printlog.PrintLog('testcli.log')
        foldername = my_printer.get_foldername()
        filename = foldername + my_printer.get_slash() + 'plotter.log'
        exists = os.path.isfile(filename)
        self.assertTrue(exists, msg='Missing plotter.log file!')
        if exists:
            with open(filename) as f:
                errors = '>>> Error' in f.read()
                self.assertFalse(errors, msg='Error in plotter.log file!')


if __name__ == '__main__':
    unittest.main(failfast=True)
