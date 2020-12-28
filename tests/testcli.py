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
from plotter import app as plotterapp

class TestRunCLI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRunClilogger(self):
        """ run scripting part of logger app """
        f = io.StringIO()
        with redirect_stdout(f):
            loggerapp.run('unittest')
        out = f.getvalue()
        out = out.splitlines()
        self.assertEqual(len(out), 8) # outputs 8 lines

    def testRunCliPlotter(self):
        """ run scripting part of plotter app """
        f = io.StringIO()
        with redirect_stdout(f):
            plotterapp.run()
        out = f.getvalue()
        out = out.splitlines()
        self.assertEqual(len(out), 4) # outputs 4 lines


if __name__ == '__main__':
    unittest.main()