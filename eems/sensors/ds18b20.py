# -*- coding: utf-8 -*-
"""
Main module for DS18B2 sensors.
"""


import os


class DS18B20(object):
    def __init__(self):
        self.path_modules = '/etc/modules'
        self.path_config = '/boot/config.txt'
        self.dir_sensors = '/sys/bus/w1/devices'

    def read(self, sensor):
        dir_file = '{}/{}'.format(self.dir_sensors, sensor)
        try:
            with open(dir_file + '/w1_slave', 'r') as slave:
                file_content = slave.readlines()
        except IOError as e:
            print e
        else:
            if file_content[0].strip()[-3:] == 'YES':
                value = file_content[1].strip()[29:]
                temp = round(float(value) / 1000, 1)
                return temp
            else:
                return 9999

    def check(self):
        if self.__check_w1_config() is True and self.__check_w1_modules() is True:
            return True
        else:
            return False

    def detect(self):
        if self.check() is True:
            return [fn for fn in os.listdir(self.dir_sensors) if fn.startswith('28')]
        else:
            return list()

    def __check_w1_config(self):
        try:
            with open(self.path_config, 'r') as config_file:
                config = config_file.readlines()
        except IOError as e:
            print e
            return False
        else:
            if len([c for c in config if c.strip('\n')[:17] == 'dtoverlay=w1-gpio']) == 0:
                return False
            else:
                return True

    def __check_w1_modules(self):
        flags = dict()
        try:
            with open(self.path_modules, 'r') as modules_file:
                modules = modules_file.readlines()
        except IOError as e:
            print e
            return False
        else:
            if len([c for c in modules if c.strip('\n') == 'w1-therm']) == 1:
                flags['w1-therm'] = True
            else:
                return False
            if len([c for c in modules if c.strip('\n') == 'w1-gpio']) == 1:
                flags['w1-gpio'] = True
            else:
                return False
            if flags['w1-therm'] is True and flags['w1-gpio'] is True:
                return True
            else:
                return False
