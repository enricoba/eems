# -*- coding: utf-8 -*-


"""
This module will handle file exports and provide functions to call for other
modules inside this package.
"""


import csv
import os
import logging
import time


class CsvHandler(object):
    def __init__(self, csv_file, logger=None):
        self.csv_file = csv_file
        self. logger = logger
        # adding simple logger ig no logger has been passed
        log_format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'
        log_date_format = '%Y-%m-%d %H:%M:%S'
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                                format=log_format,
                                datefmt=log_date_format)
            self.logger = self.logger = logging.getLogger('eems')
        else:
            self.logger = logger

    def count_col(self):
        try:
            with open(self.csv_file, 'rb') as _csv:
                csv_reader = csv.reader(_csv, delimiter=';')
                return len(csv_reader.next())
        except IOError as e:
            self.logger.error('{}'.format(e))

    def count_rows(self):
        try:
            with open(self.csv_file, 'rb') as _csv:
                csv_reader = csv.reader(_csv, delimiter=';')
                rows = sum(1 for row in csv_reader)
                return rows
        except IOError as e:
            self.logger.error('{}'.format(e))

    def add(self, header):
        if os.path.exists(self.csv_file) is False:
            if isinstance(header, list) is True:
                header = ['id', 'date', 'time'] + header
                try:
                    with open(self.csv_file, 'wb') as _csv:
                        csv_writer = csv.writer(_csv, delimiter=';')
                        csv_writer.writerow(header)
                except IOError as e:
                    self.logger.error('{}'.format(e))
            else:
                self.logger.error('Function "add" expects a list')
        else:
            self.logger.error('File {} already exists'.format(self.csv_file))

    def write(self, data):
        if os.path.exists(self.csv_file) is True:
            if isinstance(data, dict) is True:
                columns = self.count_col() - 3
                entries = len(data.keys())
                if entries == columns:
                    row = self.count_rows() - 1
                    str_date = time.strftime('%Y-%m-%d')
                    str_time = time.strftime('%H-%M-%S')
                    data = [row, str_date, str_time] + data.keys()
                    try:
                        with open(self.csv_file, 'ab') as _csv:
                            csv_writer = csv.writer(_csv, delimiter=';')
                            csv_writer.writerow(data)
                    except IOError as e:
                        self.logger.error('{}'.format(e))
                else:
                    self.logger.error('Passed elements do not have the same '
                                      'length as columns in csv')
            else:
                self.logger.error('Function "write" expects a dictionary')
        else:
            self.logger.error('File {} does not exist'.format(self.csv_file))
