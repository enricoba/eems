# -*- coding: utf-8 -*-
"""
This module provides import functions and classes to call for other modules
inside this package.
"""

import time
import numpy as np
import logging


"""
defining logger
"""

logger = logging.getLogger(__name__)


class CSV:  # TODO merge into handlers and merge imports export to handlers
    def __init__(self, csv_file, sensor_count):
        """Public function *import_data* reads a passed csv file and
        returns content, interval and duration.

        :param csv_file:
            Expects a string containing a csv file name.
        :param sensor_count:
            Expects an integer containing the amount of sensors.
        :return:
        """
        # validating the passed parameter *csv_file*
        if isinstance(csv_file, basestring) is True:
            self.csv_file = csv_file
        else:
            logger.error('Passed parameter *csv_file* is no string')

        if isinstance(sensor_count, int) is True:
            self.sensor_count = sensor_count
        else:
            logger.error('Passed parameter *sensor_count* is no integer')

        # extract content
        try:
            with open(self.csv_file, 'rb') as csv:
                    header = csv.readlines()[0].split(';')
        except IOError as e:
            logger.error('{}'.format(e))
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
