# -*- coding: utf-8 -*-
"""
Scripts for eems-server.
"""

import argparse
import sys


help_text = """Help Information for eems-server.
Usage:
  eems-server <command>
Commands:
  start             Start the eems server.
  stop              Stop the eems server.
  restart           Restart the eems server."""


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def main(eems):
    parser = ThrowingArgumentParser(add_help=False)
    parser.add_argument('command')

    try:
        args = parser.parse_args()
    except ArgumentParserError:
        print help_text
        sys.exit()

    if args.command == 'start':
        print 'start'
        eems.debug = False
        eems.run(host='0.0.0.0')

    elif args.command == 'stop':
        print 'stop'

    elif args.command == 'restart':
        print 'restart'

    else:
        print help_text
