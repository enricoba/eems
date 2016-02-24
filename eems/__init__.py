# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""

from sensors.ds18b20 import DS18B20
from main.logger import init
import logging


"""
eems project information
"""


__all__ = ['logging', 'init', 'DS18B20']
__project__ = 'eems'
__version__ = '0.1.0.5.b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'
