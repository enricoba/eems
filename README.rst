============
Introduction
============

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

Usage::

  eems <command> [options]


Show help::

   eems help

2. Python script
~~~~~~~~~~~~~~~~

Quick start::

   import eems


   # generate check-object to identify ds18b20 requirements
   c = eems.Check()
   # check if modules w1-therm and w1-gpio are set
   c.w1_modules()
   # check if dtoverlay=w1-gpio is set in config.txt
   c.w1_config()

   # generate temp-object to read sensors
   t = eems.Temp()

   # Read all connected sensors once.
   t.read_once()

   # Start reading temperature sensors with an interval of 2s and a maximum
   # duration of 10s
   t.start_read(interval=2, duration=10)

Detailed documentation still needs to be defined.