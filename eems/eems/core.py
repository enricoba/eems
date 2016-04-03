# -*- coding: utf-8 -*-
"""
Core module.
"""
# Standard modules/functions from python
import time
import logging
import os
import sys
from threading import Lock, Thread, Event
# Internal modules/functions from eems
from eems.support.checks import Check
from eems.support.detects import ds18b20_sensors
from eems.support.handlers import ConfigHandler, CsvHandler


class _SensorDictionary(object):
    def __init__(self):
        """Private class *_SensorDictionary* provides functions to manage the
        sensors dictionary.

        :return:
            Returns a in-memory object tree providing the functions
            *set_temp*, *get_dic* and *reset_dic*.
        """
        self.dic = dict()
        self.lock = Lock()

    def add_sensor(self, sensor_type, sensors):
        self.dic[sensor_type] = {sensor: None for sensor in sensors}

    def set_temp(self, sensor_type, sensor, temp):
        """Public function *set_temp* sets the value for an individual key.

        :param sensor_type:
            Expects a string of the sensor type name.
        :param sensor:
            Expects a string of the sensor name to match with the sensor key.
        :param temp:
            Expects an integer or a float containing the sensor value
            to store.
        :return:
            Returns *None*.
        """
        with self.lock:
            self.dic[sensor_type][sensor] = temp

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
        for sensor_type in self.dic:
            for sensor in self.dic[sensor_type]:
                self.dic[sensor_type][sensor] = None


class Eems(object):
    def __init__(self, sensors, log=None, console=None, csv=None):
        """

        :param log:
        :param console:
        :param csv:
        :return:
        """
        # Check sensors
        if isinstance(sensors, list) is True:
            for sensor in sensors:
                if isinstance(sensor, str) is True:
                    pass
                else:
                    logging.error('Sensor list must contain strings')
                    sys.exit()
        else:
            logging.error('Please provides sensors as list')
            sys.exit()

        # flags, handlers etc.
        __home__ = '/home/pi/eems'
        self.__config__ = ConfigHandler()
        self.__csv__ = CsvHandler(__home__)
        self.monitor_flag = False
        self.stop = False
        self.event = Event()

        c_log, c_console, c_csv = self.__config__.read_all_config()
        if log is None:
            log = c_log
        if console is None:
            console = c_console
        if csv is None:
            csv = c_csv

        # validate user input
        if isinstance(log, bool) is True:
            pass
        else:
            logging.error('Parameter *log* must be a bool')
            sys.exit()
        if isinstance(console, bool) is True:
            pass
        else:
            logging.error('Parameter *console* must be a bool')
            sys.exit()
        if isinstance(csv, bool) is True:
            pass
        else:
            logging.error('Parameter *csv* must be a bool')
            sys.exit()

        # save parameter to config file
        if log is True:
            self.__config__.set_config('general', 'log', True)
            self.__config__.write_config()
        elif log is False:
            self.__config__.set_config('general', 'log', False)
            self.__config__.write_config()
        if console is True:
            self.__config__.set_config('general', 'console', True)
            self.__config__.write_config()
        elif console is False:
            self.__config__.set_config('general', 'console', False)
            self.__config__.write_config()

        # logger
        str_date = time.strftime('%Y-%m-%d')
        str_time = time.strftime('%H-%M-%S')
        log_format = '%(asctime)-21s %(name)-22s %(levelname)-9s %(message)s'
        log_date_format = '%Y-%m-%d %H:%M:%S'
        if os.path.basename(sys.argv[0])[-3:] == '.py':
            filename_script = os.path.basename(sys.argv[0])[:-3]
        else:
            filename_script = 'eems'

        if log is True:
            log_file = '{}{}_{}_{}.txt'.format(__home__, str_date, str_time,
                                               filename_script)
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
            logger = logging.getLogger(__name__)
            logger.info('Logfile has been created')
        else:
            logging.basicConfig(level=logging.INFO,
                                format=log_format,
                                datefmt=log_date_format)
            if console is False:
                logging.disabled = True
            logger = logging.getLogger(__name__)
            logger.info('No logfile has been created')

        # determine PID and write log
        pid = os.getpid()
        logger.debug('Process PID: {}'.format(pid))

        # check sensors list + detect connected sensors
        c = Check()
        self.sensors_dict = _SensorDictionary()
        for sensor in sensors:
            if sensor.upper() == 'DS18B20':
                if c.w1_config() is True and c.w1_modules() is True:
                    tmp_sensors = ds18b20_sensors()
                    if tmp_sensors is False:
                        sys.exit()
                    else:
                        self.sensors_dict.add_sensor('DS18B20', tmp_sensors)
                else:
                    logger.error('Check for DS18B20 failed')
                    sys.exit()
            # elif sensor.upper() == 'DHT11':
            #    print 'check dht11'
            else:
                logging.warning('Sensor: {} not available'.format(sensor))

        # CSV
        if csv is True:
            # save parameter to config file
            self.csv = True
            self.__config__.set_config('exports', 'csv', True)
            self.__config__.write_config()

            csv_file = '{}_{}_{}.csv'.format(str_date, str_time,
                                             filename_script)
            csv_sensor_list = list()
            for sensor_type in self.sensors_dict.dic.keys():
                for sensor in sensor_type.keys():
                    csv_sensor_list.append('{}_{}'.format(sensor_type, sensor))

            # generate csv handler
            self.__csv__.add(csv_file, csv_sensor_list)
        elif csv is False:
            self.csv = False
            self.__config__.set_config('exports', 'csv', False)
            self.__config__.write_config()

    def monitor(self, interval=None, duration=None):
        """Public function *monitor* starts a thread to read connected
        sensors within an *interval* over a *duration*.

        :param interval:
            Expects an integer containing the *interval* time in seconds. The
            default value is defined inside the config file.
        :param duration:
            Expects an integer containing the *duration* time in seconds.
            The default value is defined in the config file. Therefore, *0*
            represents infinite. The thread can be stopped manually by
            pressing Ctrl+C or by killing the PID.
        :return:
            Returns *None*.
        """
        # validate user input
        if interval is None:
            interval = self.__config__.read_config('monitor', 'interval', 'int')
            pass
        else:
            if isinstance(interval, int) is True:
                self.__config__.set_config('monitor', 'interval', interval)
                self.__config__.write_config()
                pass
            else:
                logging.error('Parameter interval must be an integer')
                sys.exit()
        if duration is None:
            duration = self.__config__.read_config('monitor', 'duration', 'int')
            pass
        else:
            if isinstance(duration, int) is True:
                self.__config__.set_config('monitor', 'duration', duration)
                self.__config__.write_config()
                pass
            else:
                logging.error('Parameter duration must be an integer')
                sys.exit()

        if self.monitor_flag is False:
            if interval < 2:
                logging.error('Interval must be >= 2s')
                sys.exit()
            worker = Thread(target=self.__start_read, args=(interval,))
            logging.debug('Thread monitor was added')
            if duration > interval:
                watchdog = Thread(target=self.__watchdog,
                                  args=(duration, interval))
                watchdog.setDaemon(True)
                logging.debug('Watchdog_one has started with a duration'
                              ' of {}s'.format(duration))
                watchdog.start()
            else:
                logging.error('Duration must be longer than the interval')
                sys.exit()
            worker.start()
            self.monitor_flag = True
            logging.debug('Thread monitor has started with an '
                          'interval of {}s'.format(interval))
            try:
                while self.stop is False:
                    time.sleep(0.25)
            except KeyboardInterrupt:
                self.__stop(trigger='keyboard')
        else:
            logging.warning('Already one read thread is running, '
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
            self.sensors_dict.reset_dic()
            # read all connected sensor types
            for sensor_type in self.sensors_dict.dic.keys():
                tmp_sensor_dict = self.sensors_dict.dic[sensor_type]
                if sensor_type.upper() == 'DS18B20':
                    # abrufen der sensoren gleichzeitig
                    # schreiben ins dict nacheinander, dict kurz sperren
                    tmp_sensor_values = read_ds18b20(tmp_sensor_dict)
                    # main_sensor_dict sperren
                    self.sensors_dict.dic['DS18B20'] = tmp_sensor_values
                    # main_sensor_dict freigeben

                # elif sensor_type.upper() == 'DHT11':
                #     read_dht11(tmp_sensor_dict)


                # über sensor_type entsprechende sensor-funktion aufrufen
                # sensoren aus main_sensor_dict auswählen und an funktion weitergeben
                # funktion mit oben ausgewählten sensoren aufrufen
                # bekommt gefülltes dict zurück
                # gefülltest dict in main_sensor_dict einbauen/einfügen/ersetzen
                # => Read-Funktion so umbauen das dict mitgegeben werden muss



            if self.csv is True:
                # write csv
                # auf oben gefülltes dict zugreifen
                # sensoren + werte extrahieren und in csv eintragen

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
            logging.debug(message)
            self.flag = False
            self.stop = True
        else:
            logging.warning('No monitor function to stop ...')

