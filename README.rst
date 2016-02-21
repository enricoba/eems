============
Introduction
============

An easy application to establish an energy monitoring system for raspberry pi
and ds18b20 temperature sensors.


1. Installation
===============

Install via pip::

    pip install eems

Install via git::

    git clone https://github.com/enricoba/eems.git
    cd eems/
    python setup.py install

2. Usage
========

The application can be used directly in the command line or be used via API.

2.1 Command line
----------------

Usage::

  eems <command> [options]


Show help::

   eems help

2.2 API
-------

Quick start::

   import eems


   # generate check-object to identify ds18b20 requirements
   c = eems.Check()
   # check if modules w1-therm and w1-gpio are set
   c.w1_modules()
   # check if dtoverlay=w1-gpio is set in config.txt
   c.w1_config()

   # generate temp-object to read sensors
   t = eems.Temp(console=True)

   # Read all connected DS18B20 sensors once.
   t.read()

   # Start reading DS18B20 sensors with an interval of 2s and a maximum
   # duration of 10s
   t.monitor(interval=2, duration=10)

