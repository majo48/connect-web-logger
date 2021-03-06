"""
    This file contains code for querying the SQLite database
    Copyright (c) 2020 M. Jonasse (martin.jonasse@mail.ch)
"""
import sqlite3
import os
import traceback
from sys import platform
from sqlite3.dbapi2 import Connection, Cursor


class Database:
    """ SQLite database for persisting connect-web.froeling,com logging information """

    def __init__(self, printer):
        """ initialize the SQLite database """
        self.printer = printer
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

            # create table attrs (if it doesn't exist)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "attrs" (
                    "page_key"	TEXT NOT NULL UNIQUE,
                    "label"	TEXT NOT NULL,
                    "tunit"	TEXT NOT NULL,
                    PRIMARY KEY("page_key")
                );
            """)
            conn.commit()
            cursor.execute("SELECT COUNT(*) as cnt FROM attrs")
            rows = cursor.fetchall()
            if int(rows[0][0]) == 0:
                self.__fill_attrs()

            # get a list of column offsets
            logs = cursor.execute("SELECT * FROM logs LIMIT 1")
            self.log_columns = [tuple[0] for tuple in logs.description]

            # close database cursor
            conn.close()
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite CREATE TABLE error occurred:" + e.args[0])
            traceback.print_exc()

    def __get_connection(self):
        """ get SQLite connection object """
        logpath = os.path.dirname(os.path.realpath(__file__))
        if platform == "win32":
            endpath = logpath.split('\\')[-1]
            dbpath = logpath.replace('\\' + endpath, '\\database\\db.sqlite3')
        else:  # OSX and LInux
            endpath = logpath.split('/')[-1]
            dbpath = logpath.replace('/' + endpath, '/database/db.sqlite3')
        return sqlite3.connect(dbpath)

    def __fill_attrs(self):
        """ insert 49 records in the 'attrs' table """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sqls = [
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('BoilerST', 'Boiler state name', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('BoilerNR', 'Boiler state number', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Boiler01', 'Boiler temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Boiler02', 'Flue gas temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Boiler03', 'Remaining hours in heating mode till ashbox full warning appear', 'h');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Boiler04', 'ID fan control', '%');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Boiler05', 'Residual oxygen content', '%');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Boiler06', 'Boiler temperature setpoint', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Boiler07', 'Reset counter of hours till ashbox full warning appears', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed01', 'Pellet container level', '%');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed02', 'resetable t-counter:', 't');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed03', 'Resetable kg-counter:', 'kg');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed04', 'Remaining pellet amount in store room', 't');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed05', 'Minimum pellet level fuel storeroom', 't');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed06', 'Total pellet consumption', 't');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed07', 'Pellet consumption counter', 't');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed08', 'Start of 1st pellet filling', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed09', 'Start of 2nd pellet filling', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Feed10', 'Deaktivate automatical pellet outfeeder', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating01', 'Actual flow temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating02', 'Flow temperature setpoint', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating03', 'Room temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating04', 'Outside air temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating05', 'Flow temperature SP at external temperature of -10°C', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating06', 'Flow temperature SP at external temperature of +10°C', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating07', 'Desired room temperature during heating mode', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating08', 'Desired room temperature during setback mode', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating09', 'Reduction of flow temperature in setback mode', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating10', 'External temperature, at which heating circuit pump switches off in heating mode', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating11', 'External temperature, at which heating circuit pump switches off in setback mode', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating12', 'Frost protection temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Heating13', 'From which temperature at storage tank top should the overheating protection be activated', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System01', 'Boiler type', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System02', 'Facility number', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System03', 'Core module version', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System04', 'Touch Version', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System05', 'XML Version', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System06', 'System structure since', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System07', 'Connected since', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System08', 'Last signal at', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System09', 'Operation hours', 'h');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System10', 'Hours since last maintenance', 'h');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System11', 'Number of burner starts', '');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System12', 'Hours in partial load (Boiler control variable < 40 %)', 'h');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('System13', 'Hours of heating', 'h');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Tank01', 'DHW tank top temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Tank02', 'DHW tank pump control', '%');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Tank03', 'Set DHW temperature', '°C');",
            "INSERT INTO 'main'.'attrs' ('page_key', 'label', 'tunit') VALUES ('Tank04', 'Reload if DHW tank temperature is below', '°C');"
        ]
        try:
            for sql in sqls:
                cursor.execute(sql)
            conn.commit()
            conn.close()
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite INSERT person error occurred: " + e.args[0])

    def _str2int(self, str):
        """ convert string to integer value """
        try:
            return int(float(str))
        except:
            return 0

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
            self.printer.print("SQLite INSERT person error occurred: " + e.args[0])

    def count_logs(self):
        """ return the number of logs in the database """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT count(*) from logs
        """
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            row = rows[0]
            return row[0]
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(count_logs): " + e.args[0])
            return 'n/a'

    def get_first_timestamp(self):
        """ get the first (lowest) timestamp in the database """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT timestamp from logs
            LIMIT 1
        """
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            row = rows[0]
            return str(row[0])
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_first_timestamp): " + e.args[0])
            return 'n/a'

    def get_last_timestamp(self):
        """ get the last (hoghest) timestamp in the database """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT timestamp from logs
            ORDER BY timestamp DESC
            LIMIT 1
        """
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            row = rows[0]
            return str(row[0])
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_last_timestamp): " + e.args[0])
            return 'n/a'

    def get_timestamps(self, fromDate, toDate):
        """ get all time distinct timestamps after(incl.) fromDate until toDate(incl.) """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT DISTINCT timestamp from logs
            WHERE timestamp >= '?1'
            AND timestamp <= '?2'
        """
        try:
            sql = sql.replace('?1', fromDate)
            sql = sql.replace('?2', toDate)
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            return [x[0] for x in rows]  # list of strings
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_timestamps): " + e.args[0])
            return '[]'

    def get_rows_with(self, fromDate, toDate, colName):
        """ get all values with colName, after(incl.) fromDate until toDate(incl.) """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT value from logs
            WHERE timestamp >= '?1'
            AND timestamp <= '?2'
            AND page_key = '?3'
        """
        try:
            sql = sql.replace('?1', fromDate)
            sql = sql.replace('?2', toDate)
            sql = sql.replace('?3', colName)
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            return [self._str2int(y[0]) for y in rows]  # list of integer values (or None)
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_rows_with): " + e.args[0])
            return '[]'

    def get_hours(self, fromDate, toDate):
        """ get all hourly distinct timestamps after(incl.) fromDate until toDate(incl.) """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT timestamp
            FROM logs
            WHERE page_key = "Feed07"
            AND timestamp like "%00:00"
            AND timestamp >= '?1'
            AND timestamp <= '?2'
            ORDER BY timestamp ASC
        """
        try:
            sql = sql.replace('?1', fromDate)
            sql = sql.replace('?2', toDate)
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            return [x[0] for x in rows]  # list of strings
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_timestamps): " + e.args[0])
            return '[]'

    def get_hourly_consumption(self, fromDate, toDate):
        """ get the hourly consumption (kg/hour) after(incl.) fromDate until toDate(incl.) """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT ROUND(kg - LAG(kg, 1)  OVER (ORDER BY timestamp), 1) 'kgh'
            FROM (
                SELECT 
                    timestamp, value*1000 AS kg
                FROM logs
                WHERE page_key = "Feed07"
                AND timestamp like "%00:00"
                AND timestamp >= '?1'
                AND timestamp <= '?2'
                ORDER BY timestamp ASC
            ) AS kgs
        """
        try:
            sql = sql.replace('?1', fromDate)
            sql = sql.replace('?2', toDate)
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            return [self._str2int(y[0]) for y in rows]  # list of integer values (or None)
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_consumption): " + e.args[0])
            return '[]'

    def _get_last_timeslot(self):
        """ get the last timeslot in the database """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        sql = """
            SELECT * FROM logs
            WHERE timestamp = (
                SELECT timestamp FROM logs
                ORDER BY id DESC LIMIT 1
            )
        """
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.close()
            return rows
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_last_timeslot): " + e.args[0])
            return '[]'

    def _get_attrs(self):
        """ get the list of attributes in the database """
        conn: Connection = self.__get_connection()
        cursor: Cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM attrs")
            rows = cursor.fetchall()
            conn.close()
            return rows
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(get_attrs): " + e.args[0])
            return '[]'

    def check_attrs(self):
        """ compare the attrs with the last database record """
        try:
            slots = self._get_last_timeslot()
            attrs = self._get_attrs()
            diffs = []
            # check lengths
            if len(slots) != len(attrs):
                diffs.append('The number of rows read from the website is not what is expected.')
            # check attributes
            for attr in attrs:
                attr_page_key = attr[0]
                attr_label = attr[1]
                attr_tunit = attr[2]
                for slot in slots:
                    if slot[4] == attr_page_key:
                        if slot[5] != attr_label:
                            diffs.append("Label has changed in page_key: " + attr_page_key)
                        if slot[7] != attr_tunit:
                            diffs.append("Tunit has changed in page_key: " + attr_page_key)
                        break
                else:
                    diffs.append("Cannot find page_key: " + attr_page_key)
                #
            if len(diffs) > 0:
                exc_text = "Error: deviation(s) detected in the metadata read from website:\n"
                for diff in diffs:
                    exc_text += diff + "\n"
                self.printer.print(exc_text)
        #
        except sqlite3.Error as e:
            self.printer.print("SQLite SELECT error occurred(check_attrs): " + e.args[0])


if __name__ == '__main__':
    print('So sorry, the ' + os.path.basename(__file__) + ' module does not run as a standalone.')
