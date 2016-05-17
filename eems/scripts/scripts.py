# -*- coding: utf-8 -*-
"""
Scripts for eems-server.
"""

import argparse
import sys
from eems import __app__
from eems.core import define_urls


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


def run():
    define_urls(__app__)
    parser = ThrowingArgumentParser(add_help=False)
    parser.add_argument('command')

    try:
        args = parser.parse_args()
    except ArgumentParserError:
        print help_text
        sys.exit()

    if args.command == 'start':
        print 'start'
        __app__.debug = True
        __app__.run(host='0.0.0.0')

    elif args.command == 'stop':
        print 'stop'

    elif args.command == 'restart':
        print 'restart'

    else:
        print help_text

if __name__ == '__main__':
    run()
