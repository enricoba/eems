# -*- coding: utf-8 -*-
"""
logger module
"""

import time
import logging
import ConfigParser
import ast
import os
import sys
# from eems.support.checks import Check
# from eems.support.detects import detect_ds18b20_sensors
from eems.support.exports import CsvHandler
import cPickle as Pickle


class ObjectHandler(object):
    def __init__(self):
        """

        :return:
        """
        self.filename = 'data/CsvHandler.pkl'

    def save_object(self, obj):
        """

        :param obj:
        :return:
        """
        with open(self.filename, 'wb') as _output:
            Pickle.dump(obj, _output, -1)

    def load_object(self):
        """

        :return:
        """
        with open(self.filename, 'rb') as _input:
            return Pickle.load(_input)


def read_config():
    """

    :return:
    """
    config = ConfigParser.ConfigParser()
    config.read('data/config.ini')  # TODO Absoluter pfad muss getestet werden
    c_log = ast.literal_eval(config.get('general', 'log'))
    c_console = ast.literal_eval(config.get('general', 'console'))
    c_check = ast.literal_eval(config.get('general', 'check'))
    c_csv = ast.literal_eval(config.get('exports', 'csv'))
    return c_log, c_console, c_check, c_csv


def init(log=None, console=None, csv=None):
    """

    :param log:
    :param console:
    :param csv:
    :return:
    """
    c_log, c_console, c_check, c_csv = read_config()
    if log is None:
        log = c_log
    if console is None:
        console = c_console

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
        log_file = '{0}_{1}_{2}.txt'.format(str_date, str_time,
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

    # check if any sensors are connected
    # c = Check()

    # DS1820
    """if c.w1_config() is True and c.w1_modules() is True:
        pass
    else:
        sys.exit()"""

    # CSV
    if csv is None:
        csv = c_csv
    if csv is True:
        csv_file = '{0}_{1}_{2}.csv'.format(str_date,
                                            str_time,
                                            filename_script)
        """sensors = detect_ds18b20_sensors()
        if sensors is False:
            sys.exit()
        else:
            pass"""
        sensors = ['s1', 's2']
        handler = CsvHandler(csv_file, sensors)
        object_handler = ObjectHandler()
        object_handler.save_object(handler)
