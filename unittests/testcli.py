"""
    Testcases for the logger app
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
    functions:
        testRunCLI: test command line interface
"""

import unittest
import io
from contextlib import redirect_stdout
from logger import app as loggerapp
from shared import database
from plotter import app as plotterapp


class TestRunCLI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test0database(self):
        """ test if database has enough contents for plotting (2 snapshots) """
        db = database.Database()
        cnt = db.count_logs()
        self.assertGreater(cnt, 2 * 47, "Test environment is not clean!")

    def test1RunClilogger(self):
        """ run scripting part of logger app, approx. 30 secs """
        db = database.Database()
        cnt = db.count_logs()
        if cnt < + 2 * 47:
            self.skipTest("Test environment is not clean!")
        f = io.StringIO()
        with redirect_stdout(f):
            loggerapp.run('unittest')
        out = f.getvalue()
        out = out.splitlines()
        self.assertEqual(len(out), 10)  # outputs 10 lines

    def test2RunCliPlotter(self):
        """ run scripting part of plotter app """
        db = database.Database()
        cnt = db.count_logs()
        if cnt < + 2 * 47:
            self.skipTest("Test environment is not clean!")
        f = io.StringIO()
        with redirect_stdout(f):
            plotterapp.run()
        out = f.getvalue()
        out = out.splitlines()
        self.assertEqual(len(out), 4)  # outputs 4 lines


if __name__ == '__main__':
    unittest.main(failfast=True)
