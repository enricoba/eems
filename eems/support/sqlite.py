# -*- coding: utf-8 -*-
"""
SQlite3 core module
"""


import sqlite3


class DBHandler(object):
    def __init__(self):
        self.db = None
        self.conn = None
        self.c = None
        # connect to db and create cursor

    def start(self, db):
        self.db = db
        self.conn = self.connect()
        self.c = self.conn.cursor()

    def connect(self):
        conn = sqlite3.connect('data/{}.db'.format(self.db))
        return conn

    def close(self):
        self.conn.close()

    def get_session_config(self):
        self.c.execute("SELECT * FROM SESSION_CONFIG")
        values = self.c.fetchall()
        hardware = {
            'panel': values[0][0],
            'display': values[0][1],
            'icon': values[0][2],
            'color': values[0][3],
            'final': values[0][4]
        }

        software = {
            'panel': values[1][0],
            'display': values[1][1],
            'icon': values[1][2],
            'color': values[1][3],
            'final': values[1][4]
        }
        return hardware, software

    def write_session_config(self, dic, panel):
        for key in dic:
            if key != 'panel':
                self.c.execute("UPDATE SESSION_CONFIG SET {} = '{}' "
                               "WHERE PANEL_ID = '{}'".format(key.upper(),
                                                              str(dic[key]),
                                                              panel))
        self.conn.commit()

    def get_session_config_hws(self):
        self.c.execute("SELECT * FROM SESSION_CONFIG_HWS")
        values = self.c.fetchall()

        ds18b20_vars = {
            'status': values[0][1],
            'display': values[0][2],
            'list': values[0][3],
            'msg_1': values[0][4],
            'msg_2': values[0][5]
        }
        return ds18b20_vars

    def write_session_config_hws(self, ds18b20_vars):
        for key in ds18b20_vars:
            if ds18b20_vars[key] is None:
                value = ''
            else:
                value = str(ds18b20_vars[key])
            self.c.execute("UPDATE SESSION_CONFIG_HWS SET {} = '{}'"
                           .format(key.upper(), value))
        self.conn.commit()

    def add_sensor_ids_table(self, sensor):
        self.c.execute("""CREATE TABLE SENSOR_IDS_{}(
                            NAME TEXT PRIMARY KEY,
                            USER_NAME TEXT,
                            VALUE REAL
                          );""".format(sensor.upper()))

    def add_sensor_info(self, sensor_type, dic):
        for key, value in dic.iteritems():
            self.c.execute("INSERT INTO SENSOR_IDS_{} (NAME, VALUE) VALUES "
                           "('{}', {})".format(sensor_type.upper(), key, value))
        self.conn.commit()

    def get_all(self, table):
        self.c.execute("SELECT * FROM {}".format(table))
        return self.c.fetchall()

    def check_table_exist(self, table):
        self.c.execute("SELECT * FROM sqlite_master WHERE type='table' AND "
                       "name='{}'".format(table))
        if self.c.fetchall():
            return True
        else:
            return False

    def get_sensor_info(self, table):
        self.c.execute("SELECT * FROM {}".format(table))
        value = self.c.fetchall()
        tmp = dict()
        for x in value:
            tmp[x[0]] = x[-1]
        return tmp

    def get_session_config_sws(self):
        self.c.execute("SELECT * FROM SESSION_CONFIG_SWS")
        values = self.c.fetchall()
        duration = values[0][0]
        interval = values[0][1]
        return duration, interval

    def write_session_config_sws(self, duration, interval):
        self.c.execute("UPDATE SESSION_CONFIG_SWS SET DURATION = {}, "
                       "INTERVAL = {}".format(duration, interval))
        self.conn.commit()

    def write_user_sensor_names(self, table, dic):
        for key in dic:
            self.c.execute("UPDATE SENSOR_IDS_{} SET USER_NAME = {} WHERE NAME = {}".format(table, key, dic[key]))
        self.conn.commit()
"""
def header2db(self, sensors):
    # Connecting to the database file
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()

    # Creating a new SQLite table
    # Jetztiger Aufbau sieht alle Sensoren in einer Tabelle vor
    # Alternativ je Sensortyp eine Tabelle wo der Tabellenname gleich der Sensortyp ist
    c.execute('CREATE TABLE {} {} {} {} {} {} {} {}'
              .format(self.table_name,
                      'ID', 'INTEGER', 'PRIMARY KEY',
                      'TIMESTAMP', 'INTEGER',
                      'DATE TIME', 'DATE'))

    # Adding a new column without a row value
    # Alternativ zu sensors das ganze Dic aus dem core-Modul wo dann die einzelnen Sensoren
    # hier rausgegriffen werden
    for i in sensors:
        c.execute('ALTER TABLE {} ADD COLUMN {} {}'
                  .format(self.table_name,
                          str(i), 'REAL'))

    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()
"""
