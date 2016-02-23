# -*- coding: utf-8 -*-
"""
logger function
"""

import time
import logging
import ConfigParser
import ast


def read_config():
    config = ConfigParser.ConfigParser()
    config.read('data/config.ini')
    c_log = ast.literal_eval(config.get('general', 'log'))
    c_console = ast.literal_eval(config.get('general', 'console'))
    c_check = ast.literal_eval(config.get('general', 'check'))
    c_csv = ast.literal_eval(config.get('exports', 'csv'))
    return c_log, c_console, c_check, c_csv


def init(log=None, console=None, csv=None, check=None):
    c_log, c_console, c_check, c_csv = read_config()
    if log is None:
        log = c_log
    if console is None:
        console = c_console
    if check is None:
        check = c_check
    if csv is None:
        csv = c_csv

    # logger
    str_date = time.strftime('%Y-%m-%d')
    str_time = time.strftime('%H-%M-%S')
    log_format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'

    if log is True:
        log_file = '{0}_{1}_log.txt'.format(str_date, str_time)
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
            logger = logging.getLogger('eems')
        else:
            logger = logging.getLogger('eems')
        logger.debug('Logfile has been created')
    else:
        logging.basicConfig(level=logging.INFO,
                            format=log_format,
                            datefmt=log_date_format)
        if console is True:
            logger = logging.getLogger('eems')
        else:
            logger = logging.getLogger('eems')
            logger.disabled = True
        logger.debug('No logfile has been created')
    return logger

__logger__ = init()
