from ds18b20 import *
import argparse


def main():
    parser = argparse.ArgumentParser(prog='eems',
                                     usage='\n  eems <command> [options]')
    parser.add_argument('command',
                        help='Check sensor requirements.')
    # parser.add_argument('read',
    #                    help='Read sensors once.')
    # parser.add_argument('monitor',
    #                    help='Start monitoring sensors.')

    check_group = parser.add_argument_group('check_group', 'Options for check')
    check_group.add_argument('-m', '--modules', action='store_true',
                             help='Check required modules.')
    check_group.add_argument('-c', '--config', action='store_true',
                             help='Check config.txt file.')

    monitor_group = parser.add_argument_group('monitor_group',
                                              'Options for monitor')

    monitor_group.add_argument('--check', action='store_true',
                               help='Run check before monitoring.')
    monitor_group.add_argument('--csv', action='store_true',
                               help='Write values into csv file.')
    monitor_group.add_argument('--log', action='store_true',
                               help='Write log file.')
    monitor_group.add_argument('--noprint', action='store_true',
                               help='Disable console output.')
    monitor_group.add_argument('--interval',
                               help='Define measurement interval '
                                    '(default is 60s).',
                               type=int)
    monitor_group.add_argument('--duration',
                               help='Define maximum duration '
                                    '(default is infinity).',
                               type=int)

    args = parser.parse_args()
    # print args

    if args.command == 'check':
        c = Check()
        if args.modules is True:
            c.w1_modules()
        elif args.config is True:
            c.w1_config()
        else:
            c.w1_config()
            c.w1_config()

    elif args.command == 'read':
        t = Temp()
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
        if args.noprint is True:
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
        t = Temp(check=check, csv=csv, log=log, console=console)
        t.start_read(interval=interval, duration=duration)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
