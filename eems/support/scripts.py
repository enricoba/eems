# -*- coding: utf-8 -*-
"""
Scripts for eems.
"""

import argparse
import os
import sys

from eems.bla import checks
from eems.bla import ds18b20


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def read_help():
    path = os.path.dirname(ds18b20.__file__)
    try:
        with open('{0}/data/help.txt'.format(path), 'rb') as h:
            return h.read()
    except IOError as e:
        print '{}'.format(e)


def main():  # TODO add manipulation of config file & add default
    parser = ThrowingArgumentParser(add_help=False)
    parser.add_argument('command')

    # optional arguments for check
    parser.add_argument('-m', '--modules', action='store_true')
    parser.add_argument('-c', '--config', action='store_true')

    # optional arguments for monitor
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('--log', action='store_true')
    parser.add_argument('--console', action='store_true')
    parser.add_argument('-i', '--interval', type=int)
    parser.add_argument('-d', '--duration', type=int)

    try:
        args = parser.parse_args()
    except ArgumentParserError:
        print read_help()
        sys.exit()

    if args.command == 'check':
        c = checks.Check()
        if args.modules is True:
            c.w1_modules()
        elif args.config is True:
            c.w1_config()
        else:
            c.w1_modules()
            c.w1_config()

    elif args.command == 'prepare':
        c = checks.Check()
        c.w1_prepare()

    elif args.command == 'read':
        t = ds18b20.DS18B20()  # TODO: einstellungen für read überprüfen, console muss True sein
        t.read()

    elif args.command == 'monitor':
        if args.csv is True:  # TODO: csv command muss über config-file oder init abgerufen werden
            csv = True
        else:
            csv = None
        if args.log is True:  # TODO: log command muss über config-file oder init abgerufen werden
            log = True
        else:
            log = None
        if args.console is True:  # TODO: console command muss über config-file oder init abgerufen werden
            console = True
        else:
            console = None
        if args.interval:
            interval = args.interval
        else:
            interval = 60
        if args.duration:
            duration = args.duration
        else:
            duration = None
        t = ds18b20.DS18B20()
        t.monitor(interval=interval, duration=duration)
    else:
        print read_help()


if __name__ == "__main__":
    main()
