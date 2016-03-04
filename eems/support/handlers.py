# -*- coding: utf-8 -*-
"""
This module handles file exports and provides functions and classes to call
for other modules inside this package.
"""

import csv
import os
import time
import logging
import cPickle as Pickle
import ConfigParser


"""
defining logger
"""

logger = logging.getLogger(__name__)


class ConfigHandler(object):
    def __init__(self):
        self.parser = ConfigParser.ConfigParser()
        self.path_config = 'eems/data/config.ini'

    def read_all_config(self):
        self.parser.read(self.path_config)
        c_log = self.parser.getboolean('general', 'log')
        c_console = self.parser.getboolean('general', 'console')
        c_csv = self.parser.getboolean('exports', 'csv')
        return c_log, c_console, c_csv

    def read_config(self, section, option, dtype=None):
        self.parser.read(self.path_config)
        if dtype == 'bool':
            return self.parser.getboolean(section, option)
        elif dtype == 'int':
            return self.parser.getint(section, option)
        elif dtype == 'float':
            return self.parser.getfloat(section, option)
        elif dtype is None:
            return self.parser.get(section, option)

    def set_config(self, section, option, value):
        self.parser.set(section, option, value)

    def write_config(self):
        with open(self.path_config, 'wb') as config:
            self.parser.write(config)


class ObjectHandler(object):
    def __init__(self, handler):
        """

        :param handler:
        :return:
        """
        if handler == 'csv':
            self.filename = 'eems/data/CsvHandler.pkl'
        else:
            self.filename = ''

    def save_object(self, obj):
        """

        :param obj:
        :return:
        """
        with open(self.filename, 'wb') as _output:
            Pickle.dump(obj, _output, -1)

    def load_object(self):
        """

        :return:
        """
        with open(self.filename, 'rb') as _input:
            return Pickle.load(_input)


class CsvHandler(object):
    def __init__(self, csv_file, header):
        """Public class *CsvHandler* provides functions to manipulate csv files
        passed via the parameter *csv_file*. Therefore, the standard library
        module *csv* is used.

        :param csv_file:
            Expects a string containing a csv file name. If no string is
            provided, default file name *default.csv* is assumed.
        :param header:
            Expects a list containing all header elements for the csv file.
        :return:
            Returns an object providing the public function *write*.
        """
        # validating the passed parameter *csv_file*
        if isinstance(csv_file, basestring) is True:
            self.csv_file = csv_file
        else:
            self.csv_file = 'default.csv'
            logger.warning('Passed parameter *csv_file* is no string, '
                           'filename has been changed to *default.csv*')
        # adding the csv file
        self.__add(header)

    def __count_col(self):
        """Private function *__count_col* reads the csv file handled by the
         parent class and counts existing columns.

        :return:
            Returns an integer containing the count of columns.
        """
        try:
            with open(self.csv_file, 'rb') as _csv:
                csv_reader = csv.reader(_csv, delimiter=';')
                return len(csv_reader.next())
        except IOError as e:
            logger.error('{}'.format(e))

    def __count_rows(self):
        """Private function *__count_rows* reads the csv file handled by the
         parent class and counts existing rows.

        :return:
            Returns an integer containing the count of rows.
        """
        try:
            with open(self.csv_file, 'rb') as _csv:
                csv_reader = csv.reader(_csv, delimiter=';')
                rows = sum(1 for row in csv_reader)
                return rows
        except IOError as e:
            logger.error('{}'.format(e))

    def __add(self, header):
        """Private function *__add* creates the csv file using the file name of
        the string *csv_file* passed to the parent class.

        :param header:
            Expects a list containing all header elements for the csv file.
        :return:
            Returns *None*.
        """
        # validate if csv file already exists
        if os.path.exists(self.csv_file) is False:
            # validate if passed parameter *header* is a list
            if isinstance(header, list) is True:
                # adding the columns id, date and time
                header = ['id', 'timestamp', 'date', 'time'] + header
                try:
                    with open(self.csv_file, 'wb') as _csv:
                        csv_writer = csv.writer(_csv, delimiter=';')
                        csv_writer.writerow(header)
                except IOError as e:
                    logger.error('{}'.format(e))
            else:
                logger.error('Function "add" expects a list')
        else:
            logger.error('File {} already exists'.format(self.csv_file))

    def write(self, data):
        """Public function *write* adds a new row/entry to the handled csv
        file.

        :param data:
            Expects a list containing values with the same length as keys.
        :return:
            Returns *None*.
        """
        # validate if the csv file  has been created
        if os.path.exists(self.csv_file) is True:
            # validates if the passed parameter *data* is a dictionary
            if isinstance(data, list) is True:
                columns = self.__count_col() - 4
                entries = len(data)
                # validates if the amount of columns is similar to the passed
                # keys of the dictionary
                if entries == columns:
                    row = self.__count_rows()
                    tmp_time = time.localtime()
                    str_date = time.strftime('%Y-%m-%d', tmp_time)
                    str_time = time.strftime('%H:%M:%S', tmp_time)
                    timestamp = time.mktime(tmp_time)

                    data = [row, timestamp, str_date, str_time] + data
                    try:
                        with open(self.csv_file, 'ab') as _csv:
                            csv_writer = csv.writer(_csv, delimiter=';')
                            csv_writer.writerow(data)
                    except IOError as e:
                        logger.error('{}'.format(e))
                else:
                    logger.error('Passed elements do not have the same '
                                 'length as columns in csv')
            else:
                logger.error('Function "write" expects a list')
        else:
            logger.error('File {} does not exist'.format(self.csv_file))
