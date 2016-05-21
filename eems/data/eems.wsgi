#!/usr/bin/python
import sys
import logging


logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/eems/')


from eems import app as application
