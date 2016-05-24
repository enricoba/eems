# -*- coding: utf-8 -*-
"""
Script file for eems.
"""


import os
import sys
import argparse
import subprocess

from eems.support import others, sqlite


help_text = """Help Information for eems setup.
Usage:
  eems-server <command>
Commands:
  setup               Set up eems server.
  uninstall           Uninstall eems server.
  -h --help           Show help."""


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def main():
    sudo_user = os.getenv("SUDO_USER")
    if sudo_user is None:
        print "Please run eems as sudo"
        sys.exit()
    else:
        pass

    path = os.path.dirname(__file__)
    parser = ThrowingArgumentParser(add_help=False)
    parser.add_argument('command')

    try:
        args = parser.parse_args()
    except ArgumentParserError:
        print help_text
        sys.exit()

    if args.command == 'setup':
        file_path = '{}/setup.sh'.format(path)
        actual_user = others.get_user()
        subprocess.call([file_path, actual_user])
        config_db = sqlite.ConfigHandler()
        config_db.start()
        config_db.write('USER', actual_user)
        config_db.write('HOME', '/home/{}/eems'.format(actual_user))
        config_db.close()
    elif args.command == 'uninstall':
        actual_user = others.get_user()
        file_path = '{}/uninstall.sh'.format(path)
        subprocess.call([file_path, actual_user])

    else:
        print help_text


if __name__ == '__main__':
    main()
