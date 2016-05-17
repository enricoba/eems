# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""


from flask import Flask


"""
eems project information
"""

__project__ = 'eems'
__version__ = '0.2.0.1b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'
__app__ = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
