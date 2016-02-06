# -*- coding: utf-8 -*-


"""
This module will handle file exports and provide functions to call for other
modules inside this package.
"""


import csv
import os


class CsvHandler(object):
    def __init__(self, csv_file=None, logger=None):
        self.csv_file = csv_file
        self. logger = logger
        self.exist_flag = False

    def __count_col(self):
        try:
            with open(self.csv_file, 'rb') as _csv:
                csv_reader = csv.reader(_csv, delimiter=';')
                return len(csv_reader.next())
        except IOError:
            'kann nicht lesen'

    def add(self, header):
        if os.path.exists(self.csv_file) is False:
            if isinstance(header, list) is True:
                header = ['id', 'date', 'time'] + header
                try:
                    with open(self.csv_file, 'wb') as _csv:
                        csv_writer = csv.writer(_csv, delimiter=';')
                        csv_writer.writerow(header)
                except IOError:
                    print 'kann nicht lesen'
            else:
                print 'no list passed'
        else:
            print 'file schon da'

    def write(self, data):
        if os.path.exists(self.csv_file) is True:
            if isinstance(data, dict) is True:
                columns = self.__count_col()
                entries = len(data.keys())
                if entries == columns:
                    try:
                        with open(self.csv_file, 'ab') as _csv:
                            csv_writer = csv.writer(_csv, delimiter=';')
                            csv_writer.writerow(data)
                    except IOError:
                        print 'kann nicht lesen'
                else:
                    print 'nicht gleich lang'
            else:
                print 'no dict passed'
        else:
            print 'no file existing'


print os.path.exists('test.csv')
test = CsvHandler(csv_file='test.csv')
test.add(['sensor1', 'sensor2', 'sensor3'])
test.write(['1', '2016-02-05', '10:20:30', '20.3', '20.3', '10,3'])
test.write(['20'])
