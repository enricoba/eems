# -*- coding: utf-8 -*-
"""
Detects module provides functions to detect sensors.
"""

import os
import logging


"""
defining logger
"""

logger = logging.getLogger(__name__)


"""
detect ds18b20 sensors
"""


def detect_ds18b20_sensors(init=None):
    """Private function *detect_ds18b20_sensors* detects all connected DS18B20
    sensors.

    :param init:
        <tbd>
    :return:
        If sensors are detected successfully, a list containing all
        connected sensors is returned. Otherwise *None* is returned.
    """
    dir_sensors = '/sys/bus/w1/devices'
    if os.path.exists(dir_sensors):
        list_sensors = [fn for fn in os.listdir(dir_sensors)
                        if fn.startswith('28')]
        if len(list_sensors) != 0:
            if init is True:
                logger.info('DS18B20 sensors detected: {0}'.format(
                    len(list_sensors)))
            else:
                pass
            return sorted(list_sensors)
        else:
            logger.error('No DS18B20 sensors detected')
            return False
    else:
        logger.error('Path "/sys/bus/w1/devices" does not exist')
        return False
