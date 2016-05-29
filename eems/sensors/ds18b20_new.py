# -*- coding: utf-8 -*-
"""
Main module for DS18B2 sensors.
"""


import os
import logging
from threading import Thread


"""
defining logger
"""

logger = logging.getLogger(__name__)


"""
Private classes / functions
"""


class DS18B20(object):
    def __init__(self):
        # System paths
        self.dir_modules = '/etc/modules'
        self.dir_config = '/boot/config.txt'
        self.dir_sensors = '/sys/bus/w1/devices'

        # Flags
        self.detect_flag = False
        self.check_flags = {'config': False, 'modules': False}
        self.check_modules_flags = {'w1-therm': False, 'w1-gpio': False}

        # Sensor dictionaries
        self.sensor_dict = dict()

    def __flags(self):
        if self.detect_flag is True and self.check_flags['config'] is True and self.check_flags['modules'] is True:
            return True
        else:
            return False

    def detect(self):
        """Private function *detect* detects all connected DS18B20 sensors.

        :return:
            Returns a boolean.
        """
        if os.path.exists(self.dir_sensors):
            list_sensors = [fn for fn in os.listdir(self.dir_sensors) if fn.startswith('28')]
            if len(list_sensors) != 0:
                logger.info('DS18B20 sensors detected: {0}'.format(len(list_sensors)))
                self.detect_flag = True
                tmp_dict = dict()
                for sensor in list_sensors:
                    tmp_dict[sensor] = None
                self.sensor_dict = tmp_dict
                return True
            else:
                logger.error('No DS18B20 sensors detected')
                self.detect_flag = False
                return False
        else:
            logger.error('Path "/sys/bus/w1/devices" does not exist')
            self.detect_flag = False
            return False

    def check_w1_config(self):
        try:
            with open(self.dir_config, 'r') as config_file:
                config = config_file.readlines()
        except IOError as e:
            logger.error('{}'.format(e))
            self.check_flags['config'] = False
            return False
        else:
            check = [c for c in config if c.strip('\n')[:17] == 'dtoverlay=w1-gpio']
            if len(check) == 0:
                logger.error('Config.txt check failed: "dtoverlay=w1-gpio" is not set')
                logger.info('Please use the command script <sudo eems prepare> to prepare "/boot/config.txt"')
                self.check_flags['config'] = False
                return False
            else:
                logger.info('Config.txt check ok: "dtoverlay=w1-gpio" is set')
                self.check_flags['config'] = True
                return True

    def check_w1_modules(self):
        try:
            with open(self.dir_modules, 'r') as modules_file:
                modules = modules_file.readlines()
        except IOError as e:
            logger.error('{}'.format(e))
            self.check_flags['modules'] = False
            return False
        else:
            check_therm = [c for c in modules if c.strip('\n') == 'w1-therm']
            check_gpio = [c for c in modules if c.strip('\n') == 'w1-gpio']
            if len(check_therm) == 1:
                logger.info('Module check ok: "w1-therm" is set')
                self.check_modules_flags['w1-therm'] = True
            else:
                logger.error('Module check failed: "w1-therm" is not set')
            if len(check_gpio) == 1:
                logger.info('Module check ok: "w1-gpio" is set')
                self.check_modules_flags['w1-gpio'] = True
            else:
                logger.error('Module check failed: "w1-gpio" is not set')
            if self.check_modules_flags['w1-therm'] is True \
                    and self.check_modules_flags['w1-gpio'] is True:
                self.check_flags['modules'] = True
                return True
            else:
                logger.info('Please use the command script <sudo eems '
                            'prepare> to prepare "/etc/modules"')
                self.check_flags['modules'] = False
                return False

    def __read_slave(self, sensor):
        """Private function *__read_slave* reads the file *w1_slave* of a
        connected DS18B20 sensor.

        :param sensor:
            Expects a string containing the name of a connected DS18B20 sensor.
        :return:
            Returns *None*.
        """
        dir_file = '{}/{}'.format(self.dir_sensors, sensor)
        try:
            with open(dir_file + '/w1_slave', 'r') as slave:
                file_content = slave.readlines()
        except IOError as e:
            logger.error('{}'.format(e))
        else:
            if file_content[0].strip()[-3:] == 'YES':
                value = file_content[1].strip()[29:]
                t = round(float(value) / 1000, 1)
                self.sensor_dict[sensor] = t
                logger.info('Sensor: {} - read successful - {}°C'.format(sensor, t))
            else:
                logger.warning('Sensor: {} - read failed (Wrong CRC?)'.format(sensor))
                # TODO HINWEIS: kein MEsswert als "-99999" damit Tabelle als Float formatiert werden kann
                self.sensor_dict[sensor] = -99999

    def read(self):
        """Private function *__read_sensors* reads all connected DS18B20 sensors
        by initializing parallel threads. Function waits until all sensors
        are read.

        :return:
            Returns a dictionary containing sensor names and temperature values.
        """
        if self.__flags() is True:
            threads = []
            # reset dict
            for sensor in self.sensor_dict.keys():
                self.sensor_dict[sensor] = None
                threads.append(Thread(target=self.__read_slave, args=(sensor,)))
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
            return self.sensor_dict
