""" main part of the recreate app

"""
from logger import app
import sys


if __name__ == '__main__':
    """ handle functional arguments from command line interface """
    arg_cnt = len(sys.argv)
    if arg_cnt == 1:
        # no arguments
        app.run()
    elif arg_cnt == 2:
        # first argument
        app.run(sys.argv[1])
    elif arg_cnt == 3:
        # two arguments
        app.run(sys.argv[1], sys.argv[2])
    elif arg_cnt == 4:
        # three arguments
        app.run(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Error: too many arguments')