# -*- coding: utf-8 -*-
"""
This module handles file exports and provides functions and classes to call
for other modules inside this package.
"""


import csv
import os
import logging
import time


class CsvHandler(object):
    def __init__(self, csv_file, header, logger=None):
        """Public class *CsvHandler* provides functions to manipulate csv files
        passed via the parameter *csv_file*. Therefore, the standard library
        module *csv* is used.

        :param csv_file:
            Expects a string containing a csv file name. If no string is
            provided, default file name *default.csv* is assumed.
        :param header:
            Expects a list containing all header elements for the csv file.
        :param logger:
            Expects a logger object of the standard library module *logging*.
            If *logger=None*, an own logger object of the standard
            library module *logging* is added to handle outputs.
        :return:
            Returns an object providing the public function *write*.
        """
        # validating the passed parameter *logger*
        if logger is None:
            log_format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'
            log_date_format = '%Y-%m-%d %H:%M:%S'
            logging.basicConfig(level=logging.INFO,
                                format=log_format,
                                datefmt=log_date_format)
            self.logger = self.logger = logging.getLogger('eems')
        else:
            self.logger = logger

        # validating the passed parameter *csv_file*
        if isinstance(csv_file, basestring) is True:
            self.csv_file = csv_file
        else:
            self.csv_file = 'default.csv'
            self.logger.warning('Passed parameter *csv_file* was no string, '
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
            self.logger.error('{}'.format(e))

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
            self.logger.error('{}'.format(e))

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
        """Public function *write* adds a new row/entry to the handled csv
        file.

        :param data:
            Expects a dictionary containing the same keys as passed to the
            header. All values of the passed dictionary are added to the csv.
        :return:
            Returns *None*.
        """
        # validate if the csv file  has been created
        if os.path.exists(self.csv_file) is True:
            # validates if the passed parameter *data* is a dictionary
            if isinstance(data, list) is True:
                columns = self.__count_col() - 3
                entries = len(data)
                # validates if the amount of columns is similar to the passed
                # keys of the dictionary
                if entries == columns:
                    row = self.__count_rows()
                    str_date = time.strftime('%Y-%m-%d')
                    str_time = time.strftime('%H:%M:%S')
                    data = [row, str_date, str_time] + data
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
