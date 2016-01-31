====================================
eems - easy energy monitoring system
====================================

An easy application to establish an energy monitoring system for raspberry pi
and ds18b20 temperature sensors.


Installation
============

Install via pip::

    pip install eems

Install via git::

    git clone https://github.com/enricoba/eems.git
    cd eems/
    python setup.py install

Usage
=====

The application can be used directly in the command line or be imported
into a python file.

1. Command line
~~~~~~~~~~~~~~~

Usage:
  eems <command> [options]
Commands:
:what: check            :how: Check sensor requirements.
  :read:                  Read sensors once.
  monitor               Start monitoring sensors.
  help                  Show help for commands.
Options for check:
  -m, --modules         Check required modules.
  -c, --config          Check config.txt file.
  -h, --help            Show help for command check.
Options for monitor:
  --check               Run check before monitoring.
  --csv                 Write values into csv file.
  --log                 Write log file.
  --quiet               Disable console output.
  --interval <sec>      Define measurement interval (default is 60s).
  --duration <sec>      Define maximum duration (default is infinity).
  -h, --help            Show help for command monitor.


