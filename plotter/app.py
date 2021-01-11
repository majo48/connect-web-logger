"""
    top-level plotter app
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
    functions:
        run(fromDate)
"""
import sys, traceback
from shared import database
from plotter import multilineplotter
from shared import printlog


def _get_charts():
    """
        define the charts to be rendered by this app
        plots: { 'database-index': 'plot-label', ... }
    """
    return [
        {
            'filename': 'rauchgas.png',
            'plots': {
                'Boiler02': 'Flue Gas [°C]',
                'Boiler01': 'Boiler [°C]',
                'Tank02': 'DHW pump [%]'
            }
        },
        {
            'filename': 'heizen.png',
            'plots': {
                'Boiler01': 'Boiler [°C]',
                'Heating01': 'Actual flow [°C]',
                'Heating02': 'Flow setpoint [°C]',
                'Heating07': 'Room setpoint [°C]',
                'Heating03': 'Room [°C]',
                'Heating04': 'Outside [°C]'
            }
        },
        {
            'filename': 'warmwasser.png',
            'plots': {
                'Boiler01': 'Boiler [°C]',
                'Tank02': 'DHW pump [%]',
                'Tank01': 'DHW tank top [°C]',
                'Tank03': 'Tank top setpoint [°C]'
            }
        }
    ]


def run(from_date=None, to_date=None):
    """
        argument from_date may be replaced with the first timestamp
        from the database, to_date with the last timestamp
    """
    printer = printlog.PrintLog('plotter.log')
    try:
        db = database.Database(printer)
        if db.count_logs() == 0:
            printer.print('Error: no logs in the database')
        else:
            if from_date is None:
                from_date = db.get_first_timestamp()
            printer.print('First timestamp: ' + from_date)
            if to_date is None:
                to_date = db.get_last_timestamp()
            printer.print('Last timestamp: ' + to_date)
            # render charts
            for chart in _get_charts():
                filename = chart['filename']
                plots = chart['plots']
                multilineplotter.Plotter(
                    from_date,
                    to_date,
                    chart['plots'],
                    chart['filename'],
                    printer
                )
            pass
    #
    except Exception as err:
        printer.print('Error: ' + str(err))
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