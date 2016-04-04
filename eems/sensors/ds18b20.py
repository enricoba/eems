# -*- coding: utf-8 -*-
"""
Main module for DS18B2 sensors.
"""


import collections
import logging
from threading import Thread, Lock


"""
Private classes / functions
"""


class _SensorDictionary(object):
    def __init__(self, dic):
        """Private class *_SensorDictionary* provides functions to manage the
        sensors dictionary.

        :param dic:
            Expects a sensor dictionary.
        :return:
            Returns a in-memory object tree providing the functions
            *set_temp*, *get_dic* and *reset_dic*.
        """
        self.dic = collections.OrderedDict(sorted(dic.items()))
        self.lock = Lock()

    def set_temp(self, sensor, temp):
        """Public function *set_temp* sets the value for an individual key.

        :param sensor:
            Expects a string of the sensor name to match with the sensor key.
        :param temp:
            Expects an integer or a float containing the sensor value
            to store.
        :return:
            Returns *None*.
        """
        with self.lock:
            self.dic.__setitem__(sensor, temp)

    def get_dic(self):
        """Public function *get_dic* returns the sensors dictionary.

        :return:
            Returns the dictionary.
        """
        return self.dic

    def reset_dic(self):
        """Public function *reset_dic* sets all dictionary values to None.

        :return:
            Returns *None*.
        """
        for sensor in self.dic.keys():
            self.dic.__setitem__(sensor, None)


class _DS18B20(object):
    def __init__(self, sensor_dict):
        """Private class *_DS18B20* provides read functions for ds18b20 sensors.

        :param sensor_dict:
            Expects a dictionary containing sensor names.
        :return:
            Returns *None*.
        """
        self.sensor_dict = _SensorDictionary(sensor_dict)

    def __read_slave(self, sensor):
        """Private function *__read_slave* reads the file *w1_slave* of a
        connected DS18B20 sensor.

        :param sensor:
            Expects a string containing the name of a connected DS18B20 sensor.
        :return:
            Returns *None*.
        """
        dir_file = '/sys/bus/w1/devices/' + sensor
        try:
            with open(dir_file + '/w1_slave', 'r') as slave:
                file_content = slave.readlines()
        except IOError as e:
            logger.error('{}'.format(e))
        else:
            if file_content[0].strip()[-3:] == 'YES':
                value = file_content[1].strip()[29:]
                t = round(float(value) / 1000, 2)
                self.sensor_dict.set_temp(sensor, t)
                logger.info('Sensor: {} - read successful - '
                            '{}°C'.format(sensor, t))
            else:
                logger.warning('Sensor: {} - read failed '
                               '(Wrong CRC?)'.format(sensor))
                self.sensor_dict.set_temp(sensor, 'n/a')

    def read_ds18b20(self):
        """Private function *__read_sensors* reads all connected DS18B20 sensors
        by initializing parallel threads. Function waits until all sensors
        are read.

        :return:
            Returns a dictionary containing sensor names and temperature values.
        """
        threads = []
        # reset dict
        self.sensor_dict.reset_dic()
        for sensor in self.sensor_dict.dic.keys():
            threads.append(Thread(target=self.__read_slave,
                                  args=(sensor,)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()
        return self.sensor_dict.get_dic()


"""
defining logger
"""

logger = logging.getLogger(__name__)


"""
Public classes / functions
"""


def read_ds18b20(sensor_dict):
    """Public function *read_ds18b20* creates an object (_DS18B20) and executes
    a single read session of all connected sensors.

    :param sensor_dict:
        Expects a dictionary containing sensor names.
    :return:
        Returns a dictionary containing sensor names and temperature values.
    """
    ds18b20 = _DS18B20(sensor_dict)
    return ds18b20.read_ds18b20()
