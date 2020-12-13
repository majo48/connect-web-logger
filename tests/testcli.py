""" testcases for the logger app

    functions:
        testRunCLI: test command line interface
"""

import unittest
import io
from contextlib import redirect_stdout
from logger import app

class TestRunCLI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRunCLI(self):
        """ run scripting part of logger app """
        f = io.StringIO()
        with redirect_stdout(f):
            app.run('1','2','3')
        out = f.getvalue()
        out = out.splitlines()
        self.assertEqual(len(out), 3) # outputs 3 lines


if __name__ == '__main__':
    unittest.main()