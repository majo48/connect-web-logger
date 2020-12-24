"""
    This file contains code for plotting the SQLite database
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
import os, matplotlib
import matplotlib.pyplot as plt
from logger import database


class Plotter:
    """ plotter implementation """
    def __init__(self, from_date):
        db = database.Database()
        # distinct timestamps (x)
        xlist = db.get_timestamps(from_date)
        # flue temp (y)
        ylist1 = db.get_rows_with(from_date, 'Boiler02')
        # boiler temp (y)
        ylist2 = db.get_rows_with(from_date, 'Boiler01')

        # build plot
        plt.plot(xlist, ylist1)
        plt.plot(xlist, ylist2)
        plt.savefig('plot.png')
        plt.show()


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

