# -*- coding: utf-8 -*-
"""
Init module
"""

import time
import logging
import os
import sys
from eems.support.checks import Check
from eems.support.detects import detect_ds18b20_sensors
from eems.support.handlers import CsvHandler, ObjectHandler, ConfigHandler
# from eems import __init__


def init(log=None, console=None, csv=None):
    """

    :param log:
    :param console:
    :param csv:
    :return:
    """
    config_handler = ConfigHandler()
    c_log, c_console, c_csv = config_handler.read_all_config()
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
        print 'Parameter *log* must be a bool'
        sys.exit()
    if isinstance(console, bool) is True:
        pass
    else:
        print 'Parameter *console* must be a bool'
        sys.exit()
    if isinstance(csv, bool) is True:
        pass
    else:
        print 'Parameter *csv* must be a bool'
        sys.exit()

    # save parameter to config file
    if log is True:
        config_handler.set_config('general', 'log', True)
        config_handler.write_config()
    elif log is False:
        config_handler.set_config('general', 'log', False)
        config_handler.write_config()
    if console is True:
        config_handler.set_config('general', 'console', True)
        config_handler.write_config()
    elif console is False:
        config_handler.set_config('general', 'console', False)
        config_handler.write_config()

    # logger
    str_date = time.strftime('%Y-%m-%d')
    str_time = time.strftime('%H-%M-%S')
    log_format = '%(asctime)-21s %(name)-22s %(levelname)-9s %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'
    if os.path.basename(sys.argv[0])[-3:] == '.py':
        filename_script = os.path.basename(sys.argv[0])[:-3]
    else:
        filename_script = 'eems'
    path = '/home/pi/eems/'

    if log is True:
        # save parameter to config file
        config_handler.set_config('general', 'log', True)

        log_file = '{0}{1}_{2}_{3}.txt'.format(path, str_date, str_time,
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
        # save parameter to config file
        config_handler.set_config('general', 'log', False)

        logging.basicConfig(level=logging.INFO,
                            format=log_format,
                            datefmt=log_date_format)
        if console is False:
            logging.disabled = True
        logger = logging.getLogger(__name__)
        logger.info('No logfile has been created')

    # check if any sensors are connected
    c = Check()

    # DS1820
    if c.w1_config() is True and c.w1_modules() is True:
        pass
    else:
        logger.error('Check for DS18B20 failed.')
        sys.exit()

    # CSV
    if csv is True:
        # save parameter to config file
        config_handler.set_config('exports', 'csv', True)
        config_handler.write_config()

        csv_file = '{0}{1}_{2}_{3}.csv'.format(path, str_date, str_time,
                                               filename_script)
        sensors = detect_ds18b20_sensors()
        if sensors is False:
            logger.error('No DS18B20 sensors detected')
            sys.exit()
        else:
            pass

        # generate csv handler and save to pkl file
        csv_handler = CsvHandler(csv_file, sensors)
        object_handler = ObjectHandler('csv')
        object_handler.save_object(csv_handler)
    elif csv is False:
        config_handler.set_config('exports', 'csv', False)
        config_handler.write_config()

    # __init__.on()
