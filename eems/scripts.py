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
    # path = '/usr/local/lib/python2.7/dist-packages/eems/data/'
    print path
    try:
        with open('{0}/data/help.txt'.format(path), 'r') as h:
            return h.read()
    except IOError as e:
        print '{}'.format(e)


def main():
    parser = ThrowingArgumentParser(add_help=False)
    parser.add_argument('command')

    check_group = parser.add_argument_group('check_group', 'Options for check')
    check_group.add_argument('-m', '--modules', action='store_true')
    check_group.add_argument('-c', '--config', action='store_true')

    monitor_group = parser.add_argument_group('monitor_group',
                                              'Options for monitor')
    monitor_group.add_argument('--check', action='store_true')
    monitor_group.add_argument('--csv', action='store_true')
    monitor_group.add_argument('--log', action='store_true')
    monitor_group.add_argument('--quiet', action='store_true')
    monitor_group.add_argument('--interval', type=int)
    monitor_group.add_argument('--duration', type=int)

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

    elif args.command == 'read':
        t = ds18b20.Temp()
        t.read_once()

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
        if args.quiet is True:
            console = False
        else:
            console = True
        if args.interval:
            interval = args.interval
        else:
            interval = None
        if args.duration:
            duration = args.interval
        else:
            duration = None
        t = ds18b20.Temp(check=check, csv=csv, log=log, console=console)
        t.start_read(interval=interval, duration=duration)
    else:
        print read_help()


if __name__ == "__main__":
    main()
