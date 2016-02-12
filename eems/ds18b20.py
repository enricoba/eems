# -*- coding: utf-8 -*-
"""
Main module for DS18B2 sensors.
"""

import os
import time
import sys
import logging
import exports
import collections
from threading import Thread, Lock, Event


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


class Check(object):
    def __init__(self, logger=None):
        """Public class *Check* provides functions to validate system
        configuration enabling DS18B20 sensors.

        :param logger:
            Expects a logger object of the standard library module *logging*.
            If *logger=None*, an own logger object of the standard
            library module *logging* is added to handle outputs.
        :return:
            Returns an object providing the public functions *w1_config* and
            *w1_modules*.
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

        self.dir_modules = '/etc/modules'
        self.dir_config = '/boot/config.txt'
        self.flag = {'w1-therm': False,
                     'w1-gpio': False}

    def w1_config(self):
        """Public function *w1_config* checks the config.txt file for the
        entry *dtoverlay=w1-gpio*.

        :return:
            Returns *True* if check passed. Otherwise *False*.
        """
        return self.__w1_config()

    def __w1_config(self, quiet=None):
        """Private function *__w1_config* checks the config.txt file for the
        entry *dtoverlay=w1-gpio*.

        :param quiet:
            Expects the boolean *True* or *None*. If *quiet=True*, all outputs
            of the function *w1_config* are disabled.
        :return:
            Returns *True* if check passed. Otherwise *False*.
        """
        if quiet is True:
            self.logger.disabled = True
        try:
            with open(self.dir_config, 'r') as config_file:
                config = config_file.readlines()
        except IOError as e:
            self.logger.error('{}'.format(e))
        else:
            check = [c for c in config if c.strip('\n')[:17] ==
                     'dtoverlay=w1-gpio']
            if len(check) == 0:
                self.logger.error('Config.txt check failed: "dtoverlay=w1-gpio"'
                                  ' is not set')
                self.logger.info('Please use the command script <sudo eems '
                                 'prepare> to prepare "/boot/config.txt"')
                return False
            else:
                self.logger.info('Config.txt check ok: "dtoverlay=w1-gpio" '
                                 'is set')
                return True

    def w1_modules(self):
        """Public function *w1_modules* checks the file */etc/modules* for the
        entries *w1-therm* and *w1-gpio*.

        :return:
            Returns *True* if check passed. Otherwise returns *False*.
        """
        return self.__w1_modules()

    def __w1_modules(self, quiet=None):
        """Private function *__w1_modules* checks the file */etc/modules* for the
        entries *w1-therm* and *w1-gpio*.

        :param quiet:
            Expects the boolean *True* or *None*. If *quiet=True*, all outputs
            of the function *w1_modules* are disabled.
        :return:
            Returns *True* if check passed. Otherwise returns *False*.
        """
        if quiet is True:
            self.logger.disabled = True
        try:
            with open(self.dir_modules, 'r') as modules_file:
                modules = modules_file.readlines()
        except IOError as e:
            self.logger.error('{}'.format(e))
        else:
            check_therm = [c for c in modules if c.strip('\n') == 'w1-therm']
            check_gpio = [c for c in modules if c.strip('\n') == 'w1-gpio']
            if len(check_therm) == 1:
                self.logger.info('Module check ok: "w1-therm" is set')
                self.flag['w1-therm'] = True
            else:
                self.logger.error('Module check failed: "w1-therm" is not set')
            if len(check_gpio) == 1:
                self.logger.info('Module check ok: "w1-gpio" is set')
                self.flag['w1-gpio'] = True
            else:
                self.logger.error('Module check failed: "w1-gpio" is not set')
            if self.flag['w1-therm'] is True and self.flag['w1-gpio'] is True:
                return True
            else:
                self.logger.info('Please use the command script <sudo eems '
                                 'prepare> to prepare "/etc/modules"')
                return False

    def prepare(self):
        """Public function *prepare* modifies the files */boot/config.txt* and
        */etc/modules* to enable DS18B20 functionality. Function requires *sudo*
        rights!!!

        :return:
            Returns *None*.
        """
        if self.__w1_config(quiet=True) is False:
            self.logger.disabled = False
            try:
                with open(self.dir_config, 'a') as config_file:
                    config_file.write('dtoverlay=w1-gpio\n')
            except IOError as e:
                self.logger.error('{}'.format(e))
            else:
                self.logger.info('Config.txt has been prepared successfully')
        else:
            self.logger.disabled = False

        if self.__w1_modules(quiet=True) is False:
            self.logger.disabled = False
            try:
                if self.flag['w1-therm'] is False:
                    with open(self.dir_modules, 'a') as modules_file:
                        modules_file.write('w1-therm\n')
                if self.flag['w1-gpio'] is False:
                    with open(self.dir_modules, 'a') as modules_file:
                        modules_file.write('w1-gpio\n')
            except IOError as e:
                self.logger.error('{}'.format(e))
            else:
                self.logger.info('Modules have been prepared successfully')
        else:
            self.logger.disabled = False


class Temp(object):
    def __init__(self, csv=None, log=None, console=None):
        """Public Class *Temp* detects connected DS18B20 one-wire sensors
        and provides functions to read the sensors. This class uses the
        standard library module *logging* for handling outputs.

        :param csv:
            Expects the boolean *True* or *None*. If *csv=True*, a csv file is
            created in the same directory as this script. Afterwards all public
            functions of this object write entries into the csv file after
            been called.
        :param log:
            Expects the boolean *True* or *None*. If *log=True*, a .txt logfile
            is created in the same directory as this script. Therefore, all
            outputs of the *level=DEBUG* are written into the log file.
        :param console:
            Expects the boolean *True* or *None*. If *console=True*, outputs
            of the *level=INFO* are passed to the console.
        :return:
            Returns an object providing the public functions *read* and
            *monitor*.
        """
        if os.path.basename(sys.argv[0])[-3:] == '.py':
            self.filename_script = os.path.basename(sys.argv[0])[:-3]
        else:
            self.filename_script = 'eems'
        self.str_date = time.strftime('%Y-%m-%d')
        self.str_time = time.strftime('%H-%M-%S')
        self.event = Event()
        self.read_flag = Event()
        self.flag = False
        self.stop = False

        log_format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'
        log_date_format = '%Y-%m-%d %H:%M:%S'

        if log is True:
            log_file = '{0}_{1}_{2}.txt'.format(self.str_date,
                                                self.str_time,
                                                self.filename_script)
            logging.basicConfig(level=logging.DEBUG,
                                format=log_format,
                                datefmt=log_date_format,
                                filename=log_file)
            if console is True:
                console = logging.StreamHandler()
                console.setLevel(logging.INFO)
                formatter = logging.Formatter(fmt=log_format,
                                              datefmt=log_date_format)
                console.setFormatter(formatter)
                logging.getLogger('').addHandler(console)
                self.logger = logging.getLogger('eems')
            else:
                self.logger = logging.getLogger('eems')
        else:
            logging.basicConfig(level=logging.INFO,
                                format=log_format,
                                datefmt=log_date_format)
            if console is True:
                self.logger = logging.getLogger('eems')
            else:
                self.logger = logging.getLogger('eems')
                self.logger.disabled = True

        if log is True:
            self.logger.debug('Logfile has been created')
        else:
            self.logger.debug('No logfile has been created')

        pid = os.getpid()
        self.logger.debug('Process PID: {0}'.format(pid))

        sensors = self.__detect_sensors()
        if sensors is False:
            sys.exit()
        else:
            self.sensor_dict = _SensorDictionary(sensors)

        if csv is True:
            csv_file = '{0}_{1}_{2}.csv'.format(self.str_date,
                                                self.str_time,
                                                self.filename_script)
            dic = self.sensor_dict.get_dic()
            self.CsvHandler = exports.CsvHandler(csv_file,
                                                 dic.keys(),
                                                 self.logger)
            self.csv = True
        else:
            self.csv = None

    def __detect_sensors(self):
        """Private function *__detect_sensors* detects all connected DS18B20
        sensors.

        :return:
            If sensors are detected successfully, a list containing all
            connected sensors is returned. Otherwise *None* is returned.
        """
        dir_sensors = '/sys/bus/w1/devices'
        if os.path.exists(dir_sensors):
            list_sensors = [fn for fn in os.listdir(dir_sensors)
                            if fn.startswith('28')]
            if len(list_sensors) != 0:
                self.logger.info('Sensors detected: {0}'.format(
                    len(list_sensors)))
                return list_sensors
            else:
                self.logger.error('No sensors detected')
        else:
            self.logger.error('Path "/sys/bus/w1/devices" does not exist')

    def __read_slave(self, sensor):
        """Private function *__read_slave* reads the file *w1_slave* of a
        connected DS18B20 sensor.

        :param sensor:
            Expects a string containing the name of a connected DS18B20 sensor.
        :return:
            Returns *None*.
        """
        dir_file = '/sys/bus/w1/devices/' + sensor
        for x in range(4):
            try:
                with open(dir_file + '/w1_slave', 'r') as slave:
                    file_content = slave.readlines()
            except IOError as e:
                self.logger.error('{}'.format(e))
            else:
                if x == 3:
                    self.logger.warning('Sensor: {0} - read failed '
                                        '(Wrong CRC?)'.format(sensor))
                    self.sensor_dict.set_temp(sensor, 'n/a')
                elif file_content[0].strip()[-3:] == 'YES':
                    value = file_content[1].strip()[29:]
                    t = round(float(value) / 1000, 2)
                    self.sensor_dict.set_temp(sensor, t)
                    self.logger.info('Sensor: {0} - read successful - '
                                     '{1}°C'.format(sensor, t))
                    break
                else:
                    time.sleep(0.2)

    def __read_sensors(self):
        """Private function *__read_sensors* reads all connected DS18B20 sensors
        by initializing parallel threads. Function waits until all sensors
        are read.

        :return:
            Returns *None*.
        """
        self.read_flag.clear()
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
        self.read_flag.set()

    def read(self, *args, **kwargs):
        """Public function *read* reads all connected DS18B20 sensors once.

        :return:
            Returns a dictionary containing sensor names as keys and
            sensor values as values.
        """
        del args, kwargs
        if self.csv is None:
            self.sensor_dict.reset_dic()
            self.__read_sensors()
            return self.sensor_dict.get_dic()
        else:
            self.sensor_dict.reset_dic()
            self.__read_sensors()
            result = self.sensor_dict.get_dic()
            self.CsvHandler.write(result.values())
            return result

    def monitor(self, interval=60, duration=None):
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
        if self.flag is False:
            if interval < 2:
                self.logger.error('Interval must be >= 2s')
                sys.exit()
            worker = Thread(target=self.__start_read, args=(interval,))
            self.logger.debug('Thread monitor was added')
            if duration is None:
                pass
            else:
                if duration > interval:
                    watchdog = Thread(target=self.__watchdog,
                                      args=(duration, interval))
                    watchdog.setDaemon(True)
                    self.logger.debug('Watchdog_one has started with a duration'
                                      ' of {0}s'.format(duration))
                    watchdog.start()
                else:
                    self.logger.error('Duration must be longer than the '
                                      'interval')
                    sys.exit()
            worker.start()
            self.flag = True
            self.logger.debug('Thread monitor has started with an '
                              'interval of {1}s'.format(worker, interval))
            try:
                while self.stop is False:
                    time.sleep(0.25)
            except KeyboardInterrupt:
                self.read_flag.wait()
                self.__stop(trigger='keyboard')
        else:
            self.logger.warning('Already one read thread is running, '
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
        self.read_flag.wait()
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
            if self.csv is None:
                self.sensor_dict.reset_dic()
                self.__read_sensors()
            else:
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
            self.logger.debug(message)
            self.flag = False
            self.stop = True
        else:
            self.logger.warning('No monitor function to stop ...')
