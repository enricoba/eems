# -*- coding: utf-8 -*-


import time
import numpy as np
import logging


class CSV:
    def __init__(self, csv_file, sensor_count, logger=None):
        """Public function *import_data* reads a passed csv file and
        returns content, interval and duration.

        :param csv_file:
            Expects a string containing a csv file name.
        :param sensor_count:
            Expects an integer containing the amount of sensors.
        :param logger:
            Expects a logger object of the standard library module *logging*.
            If *logger=None*, an own logger object of the standard
            library module *logging* is added to handle outputs.
        :return:
        """
        # validating the passed parameter *logger*
        if logger is None:
            log_format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'
            log_date_format = '%Y-%m-%d %H:%M:%S'
            logging.basicConfig(level=logging.INFO,
                                format=log_format,
                                datefmt=log_date_format)
            self.logger = logging.getLogger('eems')
        else:
            self.logger = logger

        # validating the passed parameter *csv_file*
        if isinstance(csv_file, basestring) is True:
            self.csv_file = csv_file
        else:
            self.logger.error('Passed parameter *csv_file* is no string')

        if isinstance(sensor_count, int) is True:
            self.sensor_count = sensor_count
        else:
            self.logger.error('Passed parameter *sensor_count* is no integer')

        # extract content
        try:
            with open(self.csv_file, 'rb') as csv:
                    header = csv.readlines()[0].split(';')
        except IOError as e:
            self.logger.error('{}'.format(e))
        else:
            data_types_base = [int, float, time.struct_time, time.struct_time]
            data_types_sensors = self.sensor_count * [float]
            data_types = data_types_base + data_types_sensors
            self.content = np.genfromtxt(self.csv_file, delimiter=';',
                                         names=header, skip_header=True,
                                         dtype=data_types)

    def content(self):
        """

        :return:
        """
        return self.content

    def interval(self):
        """

        :return:
        """
        interval = self.content['timestamp'][1] - self.content['timestamp'][0]
        return interval

    def duration(self):
        """

        :return:
        """
        duration = self.content['timestamp'][-1] - self.content['timestamp'][0]
        return duration
