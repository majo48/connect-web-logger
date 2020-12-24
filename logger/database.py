"""
    This file contains code for querying the SQLite database
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
import os
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor


class Database:
    """ SQLite database for persisting connect-web.froeling,com logging information """

    def __init__(self):
        """ initialize the SQLite database """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        try:
            # create table logs (if it doesn't exist)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "logs" (
                    "id"          INTEGER NOT NULL UNIQUE,
                    "customer_id" TEXT NOT NULL,
                    "timestamp"   TEXT NOT NULL,
                    "page_id"     TEXT NOT NULL,
                    "page_key"    TEXT NOT NULL,
                    "label"       TEXT NOT NULL,
                    "value"       TEXT NOT NULL,
                    "tunit"       TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """)
            conn.commit()
            # get a list of column offsets
            logs = cursor.execute("SELECT * FROM logs LIMIT 1")
            self.log_columns = [tuple[0] for tuple in logs.description]
            # close database cursor
            conn.close()
        #
        except sqlite3.Error as e:
            print("SQLite CREATE TABLE error occurred:" + e.args[0])

    def __get_connection(self):
        """ get SQLite connection object """
        logpath = os.path.dirname(os.path.realpath(__file__))
        endpath = logpath.split('/')[-1]
        dbpath = logpath.replace( '/'+endpath, '/database/db.sqilite3')
        return sqlite3.connect(dbpath)

    def insert_log(self, log):
        """ insert one record in the 'logs' table """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            INSERT INTO logs
            (customer_id, timestamp, page_id, page_key, label, value, tunit)
            VALUES(?,?,?,?,?,?,?)
        """
        try:
            cursor.execute(
                sql, (
                    log.get('customer_id'),
                    log.get('timestamp'),
                    log.get('page_id'),
                    log.get('page_key'),
                    log.get('label'),
                    log.get('value'),
                    log.get('tunit')
                )
            )
            conn.commit()
            conn.close()
        #
        except sqlite3.Error as e:
            print("SQLite INSERT person error occurred: " + e.args[0])

    def get_first_timestamp(self):
        """ get the first (lowest) timestamp in the database """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT timestamp from logs
            LIMIT 1
        """
        try:
            cursor.execute( sql )
            rows = cursor.fetchall()
            conn.close()
            row = rows[0]
            return str(row[0])
        #
        except sqlite3.Error as e:
            print("SQLite SELECT error occurred(1): " + e.args[0])
            return 'n/a'

    def get_timestamps(self, fromDate):
        """ get all time distinct timestamps after(incl.) fromDate """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT DISTINCT timestamp from logs
            WHERE timestamp >= '?'
        """
        try:
            sql = sql.replace('?', fromDate)
            cursor.execute( sql )
            rows = cursor.fetchall()
            conn.close()
            return [x[0] for x in rows] # list of strings
        #
        except sqlite3.Error as e:
            print("SQLite SELECT error occurred(2): " + e.args[0])
            return '[]'

    def get_rows_with(self, fromDate, colName):
        """ get all values with colName, after(incl.) afterDate """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT value from logs
            WHERE timestamp >= '?1'
            AND page_key = '?2'
        """
        try:
            sql = sql.replace('?1', fromDate)
            sql = sql.replace('?2', colName)
            cursor.execute( sql )
            rows = cursor.fetchall()
            conn.close()
            return [int(y[0]) for y in rows] # list of integer values
        #
        except sqlite3.Error as e:
            print("SQLite SELECT error occurred(3): " + e.args[0])
            return '[]'


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')
