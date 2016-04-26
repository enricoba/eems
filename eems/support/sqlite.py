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
        self.c.execute('SELECT * FROM SESSION_CONFIG')
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

    def get_sensors(self, table):
        self.c.execute('SELECT * FROM {}'.format(table))
        return self.c.fetchall()




    def add_sensor_table(self, sensor):
        self.c.execute('''CREATE TABLE "{}" (`name`	        TEXT,
                                             `value`	    REAL,
                                             `user_name`	TEXT
                                             )'''.format(sensor))

    def add_sensors(self, table, sensors):
        self.c.execute("INSERT INTO {} VALUES {}".format(table, sensors))
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
