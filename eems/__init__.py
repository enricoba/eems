# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""


from support.handlers import StatusHandler, ConfigHandler, CsvHandler


"""
eems project information
"""

__project__ = 'eems'
__version__ = '0.1.0.5.b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'


"""
object variables
"""

__home__ = '/home/pi/eems/'
__flag__ = StatusHandler('init', 'csv')
__config__ = ConfigHandler()
__csv__ = CsvHandler(__home__)
