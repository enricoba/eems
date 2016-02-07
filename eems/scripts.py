# -*- coding: utf-8 -*-


import ds18b20
import argparse
import sys
import os


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


def main():
    parser = ThrowingArgumentParser(add_help=False)
    parser.add_argument('command')

    # optional arguments for check
    parser.add_argument('-m', '--modules', action='store_true')
    parser.add_argument('-c', '--config', action='store_true')

    # optional arguments for monitor
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('--log', action='store_true')
    parser.add_argument('--console', action='store_true')
    parser.add_argument('--interval', type=int)
    parser.add_argument('--duration', type=int)

    try:
        args = parser.parse_args()
    except ArgumentParserError:
        print read_help()
        sys.exit()

    if args.command == 'check':
        c = ds18b20.Check()
        if args.modules is True:
            c.w1_modules()
        elif args.config is True:
            c.w1_config()
        else:
            c.w1_config()
            c.w1_config()

    elif args.command == 'prepare':
        c = ds18b20.Check()
        c.prepare()

    elif args.command == 'read':
        t = ds18b20.Temp()
        t.read()

    elif args.command == 'monitor':
        if args.check is True:
            check = True
        else:
            check = None
        if args.csv is True:
            csv = True
        else:
            csv = None
        if args.log is True:
            log = True
        else:
            log = None
        if args.console is True:
            console = True
        else:
            console = None
        if args.interval:
            interval = args.interval
        else:
            interval = None
        if args.duration:
            duration = args.duration
        else:
            duration = None
        t = ds18b20.Temp(check=check, csv=csv, log=log, console=console)
        t.monitor(interval=interval, duration=duration)
    else:
        print read_help()


if __name__ == "__main__":
    main()
