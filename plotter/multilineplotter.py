"""
    This file contains code for plotting the SQLite database
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
import os, matplotlib
import matplotlib.pyplot as plt
import numpy as np
from logger import database
from datetime import datetime


class Plotter:
    """ plotter implementation """
    def __init__(self, from_date, plotnames={}, filename='plot.png'):
        """ init plotter """
        # open database
        db = database.Database()
        # create x axis as numpy datetime objects
        xlist = db.get_timestamps(from_date)
        xl = []
        for str in xlist:
            xl.append(datetime.strptime(str, '%Y-%m-%d %H:%M:%S'))
        x = np.array(xl)
        # create & decorate canvas
        fig, ax = plt.subplots(figsize=(11.6,8.2)) # object oriented IF
        ax.set_xlabel('Month-Day Hour')
        ax.set_ylabel('Degree Celcius')
        ax.set_title(filename)
        # create plots
        for key, value in plotnames.items():
            ylist = db.get_rows_with(from_date, key)
            if len(ylist) == 0:
                raise Exception('Invalid key('+key+') for getting a plot')
            y = np.array(ylist)
            ax.plot(x, y, label=value)
        ax.legend()
        # create output file
        fig.savefig(filename)
        fig.show()


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

