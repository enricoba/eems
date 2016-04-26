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
        tmp_dic = {
            'display': values[0][0],
            'icon': values[0][1],
            'color': values[0][2],
            'final': values[0][3]
        }
        return tmp_dic

    def write_session_config(self, dic):
        for key in dic:
            self.c.execute("UPDATE SESSION_CONFIG SET {} = '{}'"
                           "".format(key.upper(), str(dic[key])))
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

        dht11_vars = {
            'status': values[1][1],
            'display': values[1][2],
            'list': values[1][3],
            'msg_1': values[1][4],
            'msg_2': values[1][5]
        }
        return ds18b20_vars, dht11_vars

    def write_session_config_hws(self, ds18b20_vars, dht11_vars):
        print ds18b20_vars
        for key in ds18b20_vars:
            if ds18b20_vars[key] is None:
                value = ''
            else:
                value = str(ds18b20_vars[key])
            self.c.execute("UPDATE SESSION_CONFIG_HWS SET {} = '{}'"
                           "WHERE TYP_ID = 1".format(key.upper(), value))
        print dht11_vars
        for key in dht11_vars:
            if dht11_vars[key] is None:
                value = ''
            else:
                value = str(dht11_vars[key])
            self.c.execute("UPDATE SESSION_CONFIG_HWS SET {} = '{}'"
                           "WHERE TYP_ID = 2".format(key.upper(), value))
        self.conn.commit()

    def add_sensor_ids_table(self, sensor):
        self.c.execute("""CREATE TABLE SENSOR_IDS_{}(
                            NAME TEXT PRIMARY KEY,
                            USER_NAME TEXT,
                            VALUE REAL
                          );""".format(sensor.upper()))

    def add_sensor_ids(self, sensor_type, sensors):
        for sensor in sensors:
            self.c.execute("INSERT INTO SENSOR_IDS_{} (NAME) VALUES ('{}')"
                           "".format(sensor_type.upper(), sensor))
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
