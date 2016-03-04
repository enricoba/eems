# -*- coding: utf-8 -*-
"""
Main module for DS18B2 sensors.
"""

import collections
import os
import sys
import time
import logging
from eems.support.detects import detect_ds18b20_sensors
from threading import Thread, Lock, Event
from eems.support.handlers import ObjectHandler, ConfigHandler


"""
defining logger
"""

logger = logging.getLogger(__name__)


"""
Private classes / functions
"""


class _SensorDictionary(object):
    def __init__(self, sensors):
        """Private class *_SensorDictionary* provides functions to manage the
        sensors dictionary.

        :param sensors:
            Expects a list containing sensors as strings.
        :return:
            Returns a in-memory object tree providing the functions
            *set_temp*, *get_dic* and *reset_dic*.
        """
        dic = dict()
        for sensor in sensors:
            dic[sensor] = None
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


"""
Public classes / functions
"""


class DS18B20(object):
    def __init__(self):
        """Public Class *DS18B20* detects connected DS18B20 one-wire sensors
        and provides functions to read the sensors. This class uses the
        standard library module *logger* for handling outputs.

        :return:
            Returns an object providing the public functions *read* and
            *monitor*.
        """
        self.str_date = time.strftime('%Y-%m-%d')
        self.str_time = time.strftime('%H-%M-%S')
        self.event = Event()
        # self.read_flag = Event()
        self.flag = False
        self.stop = False

        pid = os.getpid()
        logger.debug('Process PID: {0}'.format(pid))

        config_handler = ConfigHandler()
        if config_handler.read_config('exports', 'csv', dtype='bool') is True:
            self.csv = True
            object_handler = ObjectHandler('csv')
            self.CsvHandler = object_handler.load_object()
        else:
            self.csv = False

        if self.csv is True:
            sensors = detect_ds18b20_sensors(init=False)
        else:
            sensors = detect_ds18b20_sensors()
        if sensors is False:
            sys.exit()
        else:
            self.sensor_dict = _SensorDictionary(sensors)

    def __read_slave(self, sensor):
        """Private function *__read_slave* reads the file *w1_slave* of a
        connected DS18B20 sensor.

        :param sensor:
            Expects a string containing the name of a connected DS18B20 sensor.
        :return:
            Returns *None*.
        """
        dir_file = '/sys/bus/w1/devices/' + sensor
        # for x in range(4):
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
                logger.info('Sensor: {0} - read successful - '
                            '{1}°C'.format(sensor, t))
            else:
                logger.warning('Sensor: {0} - read failed '
                               '(Wrong CRC?)'.format(sensor))
                self.sensor_dict.set_temp(sensor, 'n/a')

    def __read_sensors(self):
        """Private function *__read_sensors* reads all connected DS18B20 sensors
        by initializing parallel threads. Function waits until all sensors
        are read.

        :return:
            Returns *None*.
        """
        # self.read_flag.clear()
        threads = []
        dic = self.sensor_dict.get_dic()
        for sensor in dic.keys():
            threads.append(Thread(target=self.__read_slave,
                                  args=(sensor, )))
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()
        # self.read_flag.set()

    def read(self):
        """Public function *read* reads all connected DS18B20 sensors once.

        :return:
            Returns a dictionary containing sensor names as keys and
            sensor values as values.
        """
        if self.csv is False:
            self.sensor_dict.reset_dic()
            self.__read_sensors()
            return self.sensor_dict.get_dic()
        elif self.csv is True:
            self.sensor_dict.reset_dic()
            self.__read_sensors()
            result = self.sensor_dict.get_dic()
            self.CsvHandler.write(result.values())
            return result

    def monitor(self, interval=None, duration=None):
        """Public function *monitor* starts a thread to read connected
        DS18B20 sensors within an interval over a duration.

        :param interval:
            Expects an integer containing the interval time in seconds. The
            default interval is set to 60 seconds.
        :param duration:
            Expects an integer containing the duration time in seconds. If
            *duration=None*, the duration is infinite and the thread needs to
            be stopped manually by pressing Ctrl+C.
        :return:
            Returns *None*.
        """
        config_handler = ConfigHandler()

        # validate user input
        if interval is None:
            interval = config_handler.read_config('monitor', 'interval', 'int')
            pass
        else:
            if isinstance(interval, int) is True:
                config_handler.set_config('monitor', 'duration', duration)
                # config_handler.set_config('monitor', 'interval', interval)
                pass
            else:
                logger.error('Parameter *interval* must be an integer')
                sys.exit()
        if duration is None:
            duration = config_handler.read_config('monitor', 'duration', 'int')
            pass
        else:
            if isinstance(duration, int) is True:
                # config_handler.set_config('monitor', 'duration', duration)
                config_handler.set_config('monitor', 'interval', interval)
                pass
            else:
                logger.error('Parameter *duration* must be an integer')
                sys.exit()
        config_handler.write_config()

        if self.flag is False:
            if interval < 2:
                logger.error('Interval must be >= 2s')
                sys.exit()
            worker = Thread(target=self.__start_read, args=(interval,))
            logger.debug('Thread monitor was added')
            if duration > interval:
                watchdog = Thread(target=self.__watchdog,
                                  args=(duration, interval))
                watchdog.setDaemon(True)
                logger.debug('Watchdog_one has started with a duration'
                             ' of {0}s'.format(duration))
                watchdog.start()
            else:
                logger.error('Duration must be longer than the interval')
                sys.exit()
            worker.start()
            self.flag = True
            logger.debug('Thread monitor has started with an '
                         'interval of {1}s'.format(worker, interval))
            try:
                while self.stop is False:
                    time.sleep(0.25)
            except KeyboardInterrupt:
                # self.read_flag.wait()
                self.__stop(trigger='keyboard')
        else:
            logger.warning('Already one read thread is running, '
                           'start of a second thread was stopped')

    def __watchdog(self, duration, interval):
        """Private function *__watchdog* handles stopping of the function
        *monitor* if a used defined duration was passed.

        :param duration:
            Expects an integer containing the duration in seconds.
        :param interval:
            Expects an integer containing the interval in seconds.
        :return:
            Returns *None*.
        """
        timestamp = int(time.time() / interval) * interval
        timestamp += interval
        t = timestamp - time.time()
        time.sleep(duration + t)
        # self.read_flag.wait()
        self.__stop(trigger='watchdog')

    def __start_read(self, interval):
        """Private function *__start_read* manages the loop in which the
        function *__read_sensors* is called.

        :param interval:
            Expects an integer containing the interval in seconds.
        :return:
            Returns *None*.
        """
        timestamp = int(time.time() / interval) * interval
        timestamp += interval
        self.event.clear()
        while not self.event.wait(max(0, timestamp - time.time())):
            if self.csv is False:
                self.sensor_dict.reset_dic()
                self.__read_sensors()
            elif self.csv is True:
                self.sensor_dict.reset_dic()
                self.__read_sensors()
                result = self.sensor_dict.get_dic()
                self.CsvHandler.write(result.values())
            timestamp += interval

    def __stop(self, trigger):
        """Private function *__stop* stops the thread started by calling
        the function *monitor*

        :param trigger:
            Expects a string. Either *watchdog* or *keyboard* to trigger
            varying info messages.
        :return:
            Returns *None*.
        """
        message = ''
        if self.event.is_set() is False:
            self.event.set()
            if trigger == 'watchdog':
                message = 'Monitor has been stopped due to expiring duration'
            elif trigger == 'keyboard':
                message = 'Monitor has been stopped manually by ' \
                          'pressing Ctrl-C'
            logger.debug(message)
            self.flag = False
            self.stop = True
        else:
            logger.warning('No monitor function to stop ...')
