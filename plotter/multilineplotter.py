"""
    This file contains code for plotting the database contents
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from shared import database
from shared import printlog
from datetime import datetime
import matplotlib.dates as mdates


class Plotter:
    """ plotter implementation """
    def __init__(self, from_date, to_date,
                 lines={'Boiler02': 'Flue Gas [°C]'},
                 filename='plot.png',
                 printer=printlog.PrintLog()):
        """ run plotter once """

        # open database
        db = database.Database(printer)

        # create x axis as numpy datetime objects
        xlist = db.get_timestamps(from_date, to_date)
        xl = []
        for str in xlist:
            xl.append(datetime.strptime(str, '%Y-%m-%d %H:%M:%S'))
        x = np.array(xl)

        # create & decorate canvas
        fig, ax = plt.subplots(figsize=(11.6,8.2)) # object oriented IF
        ax.set_xlabel('Month-Day Hour')
        ax.set_ylabel('Degree Celcius / Percent')
        ax.set_title(filename)
        hrs = mdates.HourLocator() # every hour
        ax.xaxis.set_minor_locator(hrs)

        # create lines
        for key, value in lines.items():
            ylist = db.get_rows_with(from_date, to_date, key)
            if len(ylist) == 0:
                raise Exception('Invalid key('+key+') for getting a plot')
            y = np.array(ylist)
            ax.plot(x, y, label=value)
        ax.legend()

        # create output file
        printer.print('Created file: '+filename)
        fig.savefig(printer.get_foldername() + printer.get_slash() + filename)
        fig.show()


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

