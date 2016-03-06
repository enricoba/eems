# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""


from support.handlers import StatusHandler

"""
eems project information
"""


__flag__ = StatusHandler(False)
print 'ich bin in __init__.py'
print 'flag object ', __flag__
__project__ = 'eems'
__version__ = '0.1.0.5.b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'
