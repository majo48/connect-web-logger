""" top-level logger app

    functions:
        run(username, password, period_minutes)

"""
import sys
from logger import session


def run(username=None, password=None, period_minutes=None):
    """ argument == 'None' will be replaced with the value from the configuration file """
    try:
        from logger import local_settings
        if username == None:
            username = local_settings.username()
        print('username: ' + username)
        if password == None:
            password = local_settings.password()
        print('password: ' + password)
        if period_minutes == None:
            period_minutes = local_settings.period_minutes()
        print('period_minutes: ' + period_minutes)
        s = session.Session(local_settings.login_url(), username, password)
        pass
    except ModuleNotFoundError:
        print('ModuleNotFoundError: please copy local_settings.py.dist to local_settings.py')


def manage_arguments():
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


if __name__ == '__main__':
    manage_arguments()