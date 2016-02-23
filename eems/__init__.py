# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""

from ds18b20 import Temp, Check
from imports import read_config
import time
import logging


"""
eems project information
"""
__project__ = 'eems'
__version__ = '0.1.0.5.b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'


"""
logger function
"""


def initiate_logger(log, console):
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
    else:
        logging.basicConfig(level=logging.INFO,
                            format=log_format,
                            datefmt=log_date_format)
        if console is True:
            logger = logging.getLogger('eems')
        else:
            logger = logging.getLogger('eems')
            logger.disabled = True
    return logger


if __name__ == '__main__':
    __log, __console = read_config()
    __logger__ = initiate_logger(__log, __console)
