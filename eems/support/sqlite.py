# -*- coding: utf-8 -*-
"""
SQlite3 core module
"""


import sqlite3


class DBHandler(object):
    def __init__(self, db_path, tabel_name):
        self.db_path = db_path  # pfad + Dateiname der Datenbank
        self.table_name = tabel_name  # falls eine Tabelle für alle Sensoren

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
