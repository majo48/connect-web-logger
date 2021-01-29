"""
    This file contains code for compressing (hourly) the database contents
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from shared import database
from shared import printlog
from datetime import datetime
import matplotlib.dates as mdates


class Consumption:
    """ plotter implementation """
    def __init__(self, from_date, to_date,
                 filename='hourly.png',
                 printer=printlog.PrintLog()):
        """ run plotter once """

        # prefix filename with date
        filename = from_date[0:10] + '-' + filename

        # open database
        db = database.Database(printer)

        # create x axis as numpy datetime objects
        xlist = db.get_hours(from_date, to_date)
        xl = []
        for s in xlist:
            xl.append(datetime.strptime(s, '%Y-%m-%d %H:%M:%S'))
        x = np.array(xl)

        # create & decorate canvas
        fig, ax = plt.subplots(figsize=(11.6,8.2)) # object oriented IF
        ax.set_xlabel('Datetime')
        ax.set_ylabel('kg (pellets)')
        ax.set_title(filename) # title is filename
        ax.grid(linestyle='dotted', linewidth='0.2', color='grey') # grid

        # create hourly chart
        ylist = db.get_hourly_consumption(from_date, to_date)
        y = np.array(ylist)
        charttype = 'bar'
        if charttype == 'line':
            hrs = mdates.HourLocator()  # every hour
            ax.xaxis.set_minor_locator(hrs)  # minor ticks
            ax.plot(x, y, label='kgh (pellets)', color='brown', linestyle='solid')
            ax.legend()
        #
        elif charttype == 'bar':
            # render xaxis labels
            plt.xticks(rotation=90)
            labels = []
            for s in xlist:
                labels.append(s[:13])
            # render bar chart
            ax.bar(np.array(labels, dtype=object), y)
            # add statistics to bar chart
            kgs = 0
            for y in ylist:
                kgs += y
            hrs = len(ylist)
            avg = round(kgs / hrs * 24, 1)
            stats = ' (' + str(kgs) + ' kg in ' + str(hrs) + ' hr, avg= ' + str(avg) +' kg/day)'
            ax.set_title(filename + stats)
            ax.axhline(kgs/hrs, color='red', linewidth=2)
        #
        elif charttype == 'step':
            # see matplotlib.pyplot.step
            raise Exception('Step chart not implemented yet')
        #
        # create output file
        printer.print('Created file: '+filename)
        fig.savefig(printer.get_foldername() + printer.get_slash() + filename)
        fig.show()


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

