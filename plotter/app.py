"""
    top-level plotter app
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
    functions:
        run(fromDate)
"""
import sys
from logger import database
from plotter import multilineplotter


def run(from_date=None):
    """ argument from_date may be replaced with the first timestamp from the database """
    try:
        db = database.Database()
        if from_date == None:
            from_date = db.get_first_timestamp()
            print('First timestamp: ' + from_date)
        multilineplotter.Plotter(
            from_date,
            {
                'Boiler02': 'Flue Gas [°C]',
                'Boiler01': 'Boiler [°C]',
                'Tank02': 'DWH pump [%]'
            },
            'rauchgas.png'
        )
    except Exception as err:
        print('Error: ' + str(err))


if __name__ == '__main__':
    """ handle functional arguments from command line interface """
    arg_cnt = len(sys.argv)
    if arg_cnt == 1:
        # no arguments
        run()
    elif arg_cnt == 2:
        # first argument
        run(sys.argv[1])
    else:
        print('Error: too many arguments')
