# -*- coding: utf-8 -*-
"""
Script file for eems.
"""


import os
import sys
import argparse
import subprocess


help_text = """Help Information for eems setup.
Usage:
  eems-server <command>
Commands:
  install             Install eems server.
  uninstall           Uninstall eems server.
  -h --help           Show help."""


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def main():
    path = os.path.dirname(__file__)
    sudo_user = os.getenv("SUDO_USER")
    if sudo_user is None:
        print "Please run eems as *sudo*."
        sys.exit()
    else:
        pass

    parser = ThrowingArgumentParser(add_help=False)
    parser.add_argument('command')

    try:
        args = parser.parse_args()
    except ArgumentParserError:
        print help_text
        sys.exit()

    if args.command == 'install':
        file_path = '{}/install.sh'.format(path)
        subprocess.call([file_path])

    elif args.command == 'uninstall':
        file_path = '{}/uninstall.sh'.format(path)
        subprocess.call([file_path])

    else:
        print help_text


if __name__ == '__main__':
    main()
