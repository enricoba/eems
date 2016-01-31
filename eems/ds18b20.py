#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import sys
import logging
from threading import Thread, Lock, Event


"""
Internal classes / functions
"""


class _SensorDictionary(object):
    def __init__(self, sensors):
        """Internal class:_SensorDictionary provides functions to manage the
        sensors dictionary.

        :param sensors:
            Expects a list containing sensors as strings.

        :return:
            Returns a in-memory object tree providing the functions
            set_temp(sensor, temp), get_dic() and reset_dic().
        """
        self.sensors = sensors
        self.dic = dict()
        for sensor in sensors:
            self.dic[sensor] = None
        self.lock = Lock()

    def set_temp(self, sensor, temp):
        """Public function:set_temp sets the value for a special key.

        :param sensor:
            Expects the string of a sensor name to match with the sensor key.

        :param temp:
            Expects a temperature value to store the value.

        :return:
            Returns None.
        """
        with self.lock:
            self.dic[sensor] = temp

    def get_dic(self):
        """Public function:get_dic returns the sensors dictionary.

        :return:
            Returns the dictionary.
        """
        return self.dic

    def reset_dic(self):
        """Public function:reset_dic is setting all dictionary values to None.

        :return:
            Returns None.
        """
        self.dic = dict()
        for sensor in self.sensors:
            self.dic[sensor] = None


"""
public class
"""


class Check(object):
    def __init__(self, logger=None):
        """Public class:Check provides public functions to check system
        configuration to make DS18B20 sensors readable.

        :param logger:
            Logger expects a logging object.

        :return:
            Returns an in-memory object tree providing the public functions
            w1_config() and w1_modules().
        """
        log_format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'
        log_date_format = '%Y-%m-%d %H:%M:%S'
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                                format=log_format,
                                datefmt=log_date_format)
            self.logger = self.logger = logging.getLogger('eems')
        else:
            self.logger = logger

    def w1_config(self):
        """Public function:w1_config checks the config.txt file for the
        entry 'dtoverlay=w1-gpio'.

        :return:
            Returns True if check passed. Otherwise None.
        """
        dir_config = '/boot/config.txt'
        try:
            with open(dir_config, 'r') as config_file:
                config = config_file.readlines()
        except IOError as e:
            self.logger.error('{}'.format(e))
            # self.logger.warning('Application has been stopped')
        else:
            check = [c for c in config if c.strip('\n') == 'dtoverlay=w1-gpio']
            if len(check) == 0:
                self.logger.error('Config.txt check failed: "dtoverlay=w1-gpio"'
                                  ' is not set')
                # self.logger.warning('Application has been stopped')
                sys.exit()
            else:
                self.logger.info('Config.txt check ok: "dtoverlay=w1-gpio" '
                                 'is set')
                return True

    def w1_modules(self):
        """Public function:w1_modules checks the file modules for the entries
        'w1-therm' and 'w1-gpio'.

        :return:
            Returns True if check passed. Otherwise None.
        """
        dir_modules = '/etc/modules'
        try:
            with open(dir_modules, 'r') as modules_file:
                modules = modules_file.readlines()
        except IOError as e:
            self.logger.error('{}'.format(e))
            # self.logger.warning('Application has been stopped')
        else:
            check = [c for c in modules if c.strip('\n') == 'w1-therm' or
                     c.strip('\n') == 'w1-gpio']
            if len(check) == 2:
                self.logger.info('Modules check ok: "w1-gpio" and "w1-therm" '
                                 'are set')
                return True
            else:
                self.logger.error('Modules check failed: "w1-gpio" and/or '
                                  '"w1-therm" are/is not set')
                # self.logger.warning('Application has been stopped')
                sys.exit()


class Temp(object):
    def __init__(self, check=None, csv=None, log=None, console=True):
        """Public Class:Temp detects all connected DS18B20 one-wire sensors
        and provides public functions to read the sensors.

        On creation of the object a logger is added. All outputs are
        managed by the internal logger.

        All connected DS18B20 sensors are detected and a dictionary
        containing the sensors is created.

        Depending on listed parameters, several functions of the object are
        activated.

        :param check:
            If check=True, the public class:Check is initialised and both public
            functions, w1_config() and w1_modules() are called.

        :param csv:
            If csv=True, an export file in csv-format is created in the same
            directory as this script. Afterwards all public functions of this
            object write an entry into the csv-file after been called.

        :param log:
            Initially log=None. A logfile in .log-format can be
            created in the same directory as this script. All outputs of the
            logger are written into the log-file. The logfile records with
            the level=DEBUG. If log=True, a logfile is created.

        :param console:
            Initially console=True. Consequently, outputs are written into the
            console. The logger level for the console is INFO. If console=False,
            no output is written into the console.

        :return:
            Returns an in-memory object tree providing the public functions
            read_once(), start_read() and stop_read().
        """
        # Adding logger
        if os.path.basename(sys.argv[0])[-3:] == '.py':
            self.filename_script = os.path.basename(sys.argv[0])[:-3]
        else:
            self.filename_script = 'eems'
        self.str_date = time.strftime('%Y-%m-%d')
        self.str_time = time.strftime('%H-%M-%S')
        self.event = Event()
        self.read_flag = Event()
        self.flag = False

        log_format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'
        log_date_format = '%Y-%m-%d %H:%M:%S'

        # logger
        if log is True:
            log_file = '{0}_{1}_{2}.log'.format(self.str_date,
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
            if console is False:
                self.logger = logging.getLogger('eems')
                self.logger.disabled = True
            else:
                self.logger = logging.getLogger('eems')

        if log is True:
            self.logger.debug('Logfile has been created')
        elif log is False:
            self.logger.debug('No logfile has been created')
        else:
            pass

        # get process PID and log
        pid = os.getpid()
        self.logger.debug('Process PID: {0}'.format(pid))

        # Run checks if check=True
        if check is True:
            check = Check(self.logger)
            if check.w1_config() is True:
                pass
            if check.w1_modules() is True:
                pass

        # Detect connected sensors and create public dictionary
        self.sensors = self.__check_sensors()
        self.sensor_dict = _SensorDictionary(self.sensors)

        # Create csv-export file if csv=True
        if csv is True:
            self.csv = True
            self.csv_filename = '{0}_{1}_{2}.csv'\
                .format(self.str_date, self.str_time, self.filename_script)
            self.__prepare_csv()
        else:
            self.csv = None
            self.csv_filename = None

    def __check_sensors(self):
        """Internal function:__check_sensors detects all connected sensors.

        :return:
            Returns a list containing all connected sensors.
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
                # self.logger.warning('Application has been stopped')
                sys.exit()
        else:
            self.logger.error('Path "/sys/bus/w1/devices" does not exist')
            # self.logger.warning('Application has been stopped')
            sys.exit()

    def __read_slave(self, sensor):
        """Internal function:__read_slave reads the file 'w1_slave' of a
        connected sensor.

        :param sensor:
            Expects a string argument containing the name of a connected sensor.

        :return:
            Returns None. On success the temperature value of the read sensor is
            passed into the public dictionary-object:sensor_dict by matching the
            dictionary keys with the sensor string argument.
        """
        dir_file = '/sys/bus/w1/devices/' + sensor
        for x in range(4):
            try:
                with open(dir_file + '/w1_slave', 'r') as slave:
                    file_content = slave.readlines()
            except IOError as e:
                self.logger.error('{}'.format(e))
                # self.logger.warning('Application has been stopped')
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
        """Internal function:__read_sensors reads all connected sensors by
        initializing parallel threads. Function waits until all sensors
        are read.

        :return:
            Returns None.
        """
        self.read_flag.clear()
        threads = []
        for x in range(len(self.sensors)):
            threads.append(Thread(target=self.__read_slave,
                                  args=(self.sensors[x], )))
            self.logger.debug('Thread for sensor {0} was '
                              'added'.format(self.sensors[x]))
        for t in threads:
            t.setDaemon(True)
            t.start()
            self.logger.debug('Thread {0} has started'.format(t))
        for t in threads:
            t.join()
            self.logger.debug('Thread {0} has joined'.format(t))
        self.read_flag.set()

    def __prepare_csv(self):
        """Internal function:__prepare_csv adds a csv-export file to store
        read values of the sensors.

        :return:
            Returns None.
        """
        str_head = ''
        for x in range(len(self.sensors)):
            if x + 1 == len(self.sensors):
                str_head = '{0}{1}'.format(str_head, self.sensors[x])
            else:
                str_head = '{0}{1};'.format(str_head, self.sensors[x])
        try:
            with open(self.csv_filename, 'a') as csv:
                csv.write('Date;Time;{0}\n'.format(str_head))
        except IOError as e:
            self.logger.error('{}'.format(e))
            # self.logger.warning('Application has been stopped')

    def __write_csv(self):
        """Internal function:__write_csv writes values into the csv-export
        file.

        :return:
            Returns None.
        """
        results = self.sensor_dict.get_dic()
        str_temp = ''
        str_date = time.strftime('%Y-%m-%d')
        str_time = time.strftime('%H:%M:%S')
        for x in range(len(self.sensors)):
            if x + 1 == len(self.sensors):
                str_temp = '{0}{1}'.format(str_temp,
                                           results[self.sensors[x]])
            else:
                str_temp = '{0}{1};'.format(str_temp,
                                            results[self.sensors[x]])
        try:
            with open(self.csv_filename, 'a') as csv:
                csv.write('{0};{1};{2}\n'.format(str_date, str_time, str_temp))
        except IOError as e:
            self.logger.error('{}'.format(e))
            # self.logger.warning('Application has been stopped')

    def read_once(self, *args, **kwargs):
        """Public function:read_one reads all connected sensors.

        If attribute internal variable:csv=True, the results are
        written into the created csv-export file. If internal
        variable:csv=None, nothing is written into any file.

        :return:
            Returns a dictionary containing sensor names as keys and
            temperatures as values.
        """
        del args, kwargs
        if self.csv is None:
            self.sensor_dict.reset_dic()
            self.__read_sensors()
            return self.sensor_dict.get_dic()
        else:
            self.sensor_dict.reset_dic()
            self.__read_sensors()
            self.__write_csv()
            return self.sensor_dict.get_dic()

    def start_read(self, interval=None, duration=None):
        """Public function:start_read starts a thread to read connected
        sensors within an specified interval.

        :param interval:
            If interval=None, the interval time is set to 60 seconds. Otherwise
            an integer is expected telling the interval time.

        :param duration:
            If duration=None, the duration is infinite and the thread needs to
            be stopped manually. Otherwise an integer is expected to determine
            maximum duration.

        :return:
            Returns None.
        """
        if self.flag is False:
            if interval is None:
                interval = 60
            elif interval < 2:
                self.logger.error('Interval must be >= 2s')
                # self.logger.warning('Application has been stopped')
                sys.exit()
            worker = Thread(target=self.__start_read, args=(interval,))
            self.logger.debug('Thread start_read was added')
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
                    self.logger.error('Duration must be longer then the '
                                      'interval')
                    # self.logger.warning('Application has been stopped')
                    sys.exit()
            # if daemon is True:
            # worker.setDaemon(True)
            # self.logger.debug('Thread start_read was set daemon=True')
            worker.start()
            self.flag = True
            self.logger.debug('Thread start_read has started with an '
                              'interval of {1}s'.format(worker, interval))
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.read_flag.wait()
                self.stop_read(trigger='keyboard')
            # finally:
                # self.logger.info('Application has been stopped')
        else:
            self.logger.warning('Already one read thread is running, '
                                'start of a second thread was stopped')

    def __watchdog(self, duration, interval):
        """Internal function:__watchdog stops the read process after a defined
        duration.

        :param duration:
            Expects an integer for the duration.

        :param interval:
            Expects an integer for the interval.

        :return:
            Returns None.
        """
        timestamp = int(time.time() / interval) * interval
        timestamp += interval
        t = timestamp - time.time()
        time.sleep(duration + t)
        self.read_flag.wait()
        self.stop_read(trigger='watchdog')

    def __start_read(self, interval):
        """Internal function:__start_read manages the loop in which the
        internal function:__read_sensors is called.

        :param interval:
            Expects an integer for the interval.

        :return:
            Returns None.
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
                self.__write_csv()
            timestamp += interval

    def stop_read(self, trigger):
        """Public function:stop_read stops the started thread to read the
        connected sensors in a fixed interval.

        :param trigger:
            Expects either 'watchdog' or 'keyboard' to trigger varying info
            messages.

        :return:
            Returns None.
        """
        message = ''
        if self.event.is_set() is False:
            self.event.set()
            if trigger == 'watchdog':
                message = 'Function:start_read has been stopped due to ' \
                          'expiring duration'
            elif trigger == 'keyboard':
                message = 'Function:start_read has been stopped manually by ' \
                          'pressing Ctrl-C'
            self.logger.info(message)
            self.flag = False
        else:
            self.logger.warning('No read function to stop ...')
