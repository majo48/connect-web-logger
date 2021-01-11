"""
    This file contains code for printing to stdout and logfiles
    This method is preferred above redirecting stdout (better control)
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""

import os
from sys import platform
from shared import local_settings


class PrintLog:
    """ enable printing to stdout and appending to a logfile """

    def __init__(self, filename=None):
        """
            initialize printing to stdout and writing to logfile
        """
        if filename is not None:
            sharedpath = os.path.dirname(os.path.realpath(__file__))
            endpath = sharedpath.split(self.get_slash())[-1]
            self.logfolder = sharedpath.replace(endpath, "logs")
            self.logfile = self.logfolder + self.get_slash() + filename
            # make folder if it doesn't exist
            if not os.path.exists(self.logfolder):
                os.makedirs(self.logfolder)
        pass # filename is None

    def print(self, txt):
        """
            print text to stdout (conditional) and
            write one line in a logfile
        """
        if local_settings.is_verbose():
            print(txt)
        with open(self.logfile, "a") as f:
            f.write(txt + "\n")

    def get_foldername(self):
        """
            get the fully qualified foldername for logs & plots
        """
        return self.logfolder

    def get_slash(self):
        """
            get the platform dependant slash
        """
        if platform == "win32":
            return '\\'
        else:
            return '/'
