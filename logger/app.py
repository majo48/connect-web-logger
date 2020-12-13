""" top-level logger app

    functions:
        run(username, password, period_minutes)

"""
import sys


def run(username='default', password='default', period_minutes='default'):
    """ argument == 'default' will take value from configuration file """
    print('username: '+username)
    print('password: '+password)
    print('period_minutes: '+period_minutes)


if __name__ == '__main__':
    """ handle functional arguments from command line interface """
    arg_cnt = len(sys.argv)
    if arg_cnt == 1:
        # no arguments
        run()
    elif arg_cnt == 2:
        # first argument
        run(sys.argv[1])
    elif arg_cnt == 3:
        # two arguments
        run(sys.argv[1], sys.argv[2])
    elif arg_cnt == 4:
        # three arguments
        run(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Error: too many arguments')