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


def get_charts():
    """
        define the charts to be rendered by this app
        plots: { 'database-index': 'plot-label', ... }
    """
    return [
        {
            'filename': 'rauchgas.png',
            'lines': [
                {'dbid': 'Boiler02', 'label': 'Flue Gas [°C]', 'color': 'brown', 'style': 'solid'},
                {'dbid': 'Boiler01', 'label': 'Boiler [°C]', 'color': 'orange', 'style': 'solid'},
                {'dbid': 'Heating02', 'label': 'Flow setpoint [°C]', 'color': 'darkviolet', 'style': 'dashed'},
                {'dbid': 'Tank02', 'label': 'DHW pump [%]', 'color': 'lime', 'style': 'dashed'}
            ]
        },
        {
            'filename': 'heizen.png',
            'lines': [
                {'dbid': 'Boiler01', 'label': 'Boiler [°C]', 'color': 'orange', 'style': 'solid'},
                {'dbid': 'Heating02', 'label': 'Flow setpoint [°C]', 'color': 'red', 'style': 'dashed'},
                {'dbid': 'Heating01', 'label': 'Actual flow [°C]', 'color': 'red', 'style': 'solid'},
                {'dbid': 'Heating07', 'label': 'Room setpoint [°C]', 'color': 'blue', 'style': 'dashed'},
                {'dbid': 'Heating03', 'label': 'Room [°C]', 'color': 'blue', 'style': 'solid'},
                {'dbid': 'Heating04', 'label': 'Outside [°C]', 'color': 'black', 'style': 'solid'}
            ]
        },
        {
            'filename': 'warmwasser.png',
            'lines': [
                {'dbid': 'Boiler01', 'label': 'Boiler [°C]','color': 'orange', 'style': 'solid'},
                {'dbid': 'Tank02', 'label': 'DHW pump [%]','color': 'lime', 'style': 'dashed'},
                {'dbid': 'Tank03', 'label': 'Tank top setpoint [°C]', 'color': 'blue', 'style': 'dashed'},
                {'dbid': 'Tank01', 'label': 'DHW tank top [°C]','color': 'blue', 'style': 'solid'}
            ]
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
            for chart in get_charts():
                multilineplotter.Plotter(
                    from_date,
                    to_date,
                    chart['lines'],
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