from ds18b20 import Temp, Check
import ConfigParser
import ast


__project__ = 'eems'
__version__ = '0.1.0.5.b1'
__copyright__ = '2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'


config = ConfigParser.ConfigParser()
config.read('data/eems.ini')  # TODO muss noch in package data geladen werden
print config.sections()
log = ast.literal_eval(config.get('log', 'log'))


# TODO define central logger
