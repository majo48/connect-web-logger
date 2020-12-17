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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "logs" (
                    "id"          INTEGER NOT NULL UNIQUE,
                    "customer_id" TEXT NOT NULL,
                    "timestamp"   TEXT NOT NULL,
                    "page_id"     TEXT NOT NULL,
                    "label"       TEXT NOT NULL,
                    "value"       TEXT NOT NULL,
                    "tunit"       TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """)
            conn.commit()
            conn.close()
        #
        except sqlite3.Error as e:
            print("SQLite CREATE TABLE error occurred:" + e.args[0])

    def __get_connection(self):
        """ get SQLite connection object """
        path = os.path.dirname(os.path.realpath(__file__))
        return sqlite3.connect(path + '/' + 'db.sqlite3')

    def insert_log(self, log):
        """ insert one record in the 'logs' table """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            INSERT INTO logs
            (customer_id, timestamp, page_id, label, value, tunit)
            VALUES(?,?,?,?,?,?)
        """
        try:
            cursor.execute(
                sql, (
                    log.get('customer_id'),
                    log.get('timestamp'),
                    log.get('page_id'),
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


if __name__ == '__main__':
    print('sorry, this does not run as a standalone')
