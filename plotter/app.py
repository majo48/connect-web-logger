"""
    top-level plotter app
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
    functions:
        run(fromDate)
"""
import sys, traceback
from logger import database
from plotter import multilineplotter


def run(from_date=None, to_date=None):
    """ argument from_date may be replaced with the first timestamp from the database """
    try:
        db = database.Database()
        if db.count_logs() == 0:
            print('Error: no logs in the database')
        else:
            if from_date == None:
                from_date = db.get_first_timestamp()
            print('First timestamp: ' + from_date)
            if to_date == None:
                to_date = db.get_last_timestamp()
            print('Last timestamp: ' + to_date)
            multilineplotter.Plotter(
                from_date,
                to_date,
                {
                    'Boiler02': 'Flue Gas [°C]',
                    'Boiler01': 'Boiler [°C]',
                    'Tank02': 'DWH pump [%]'
                },
                'rauchgas.png'
            )
            multilineplotter.Plotter(
                from_date,
                to_date,
                {
                    'Boiler01': 'Boiler [°C]',
                    'Heating01': 'Actual flow [°C]',
                    'Heating02': 'Flow setpoint [°C]',
                    'Heating07': 'Room setpoint [°C]',
                    'Heating03': 'Room [°C]',
                    'Heating04': 'Outside [°C]'
                },
                'heizen.png'
            )
            multilineplotter.Plotter(
                from_date,
                to_date,
                {
                    'Boiler01': 'Boiler [°C]',
                    'Tank02': 'DWH pump [%]',
                    'Tank01': 'DWH tank top [°C]',
                    'Tank03': 'Tank top setpoint [°C]'
                },
                'warmwasser.png'
            )

    except Exception as err:
        print('Error: ' + str(err))
        traceback.print_exc()


def manage_arguments():
    """ handle functional arguments from command line interface """
    arg_cnt = len(sys.argv)
    if arg_cnt == 1:
        # no arguments
        run()
    elif arg_cnt == 2:
        # first argument (from_date)
        run(sys.argv[1])
    elif arg_cnt == 3:
        # two arguments (from_date, to_date)
        run(sys.argv[1], sys.argv[2])
    else:
        print('Error: too many arguments')


if __name__ == '__main__':
    """ handle functional arguments from command line interface """
    manage_arguments()