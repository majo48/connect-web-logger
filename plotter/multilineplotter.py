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
    def __init__(self, from_date, to_date, lines,
                 filename='plot.png',
                 printer=printlog.PrintLog()):
        """ run plotter once """

        # prefix filename with date
        filename = from_date[0:10] + '-' + filename

        # open database
        db = database.Database(printer)

        # create x axis as numpy datetime objects
        xlist = db.get_timestamps(from_date, to_date)
        xl = []
        for s in xlist:
            xl.append(datetime.strptime(s, '%Y-%m-%d %H:%M:%S'))
        x = np.array(xl)

        # create & decorate canvas
        fig, ax = plt.subplots(figsize=(11.6,8.2)) # object oriented IF
        ax.set_xlabel('Month-Day Hour')
        ax.set_ylabel('Degree Celcius / Percent')
        ax.set_title(filename) # title is filename
        hrs = mdates.HourLocator() # every hour
        ax.xaxis.set_minor_locator(hrs) # minor ticks
        ax.grid(linestyle='dotted', linewidth='0.2', color='grey') # grid

        # create multiline plot
        for line in lines:
            ylist = db.get_rows_with(from_date, to_date, line['dbid'])
            if len(ylist) == 0:
                raise Exception('Invalid key('+line['dbid']+') for getting a plot')
            y = np.array(ylist)
            ax.plot(x, y, label=line['label'], color=line['color'], linestyle=line['style'])
        ax.legend()

        # create output file
        printer.print('Created file: '+filename)
        fig.savefig(printer.get_foldername() + printer.get_slash() + filename)
        fig.show()


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

