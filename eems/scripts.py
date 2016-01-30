from ds18b20 import *
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='Help Information for eems.',
                                     prog='eems',
                                     usage='eems <command> [options]')

    parser.add_argument('check',
                        help='Check sensor requirements.',
                        type=bool)
    parser.add_argument('monitor',
                        help='Start monitoring sensors.')
    parser.add_argument('read',
                        help='Read sensors once.')

    check_group = parser.add_argument_group('check_group', 'Options for check')
    check_group.add_argument('-m', '--modules',
                             help='Check required modules.')
    check_group.add_argument('-c', '--config',
                             help='Check config.txt file.')

    monitor_group = parser.add_argument_group('monitor_group', 'Options for monitor')

    monitor_group.add_argument('--check',
                               help='Run check before monitoring.')
    monitor_group.add_argument('--csv',
                               help='Write values into csv file.')
    monitor_group.add_argument('--log',
                               help='Write log file.')
    monitor_group.add_argument('--noprint',
                               help='Disable console output.')
    monitor_group.add_argument('--interval',
                               help='Define measurement interval (default is 60s).',
                               type=int)
    monitor_group.add_argument('--duration',
                               help='Define maximum duration (default is infinity).',
                               type=int)
    parser.print_help()
    args = parser.parse_args()

    #print args

if __name__ == "__main__":
    main()
