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
        xlist = [x[:-3] for x in xlist]  # remove seconds
        # flue temp (y)
        ylist1 = db.get_rows_with(from_date, 'Boiler02')
        # boiler temp (y)
        ylist2 = db.get_rows_with(from_date, 'Boiler01')

        fig, ax = plt.subplots(figsize=(11.6,8.2)) # object oriented IF
        ax.plot(xlist, ylist1, label='Rauchgas')
        ax.plot(xlist, ylist2, label='Boiler')
        ax.legend()

        fig.savefig('plot.png')
        fig.show()

if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')

