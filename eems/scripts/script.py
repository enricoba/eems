# -*- coding: utf-8 -*-
"""
Script file for eems.
"""


import os
import sys
import argparse
import subprocess


path = os.path.dirname(__file__)


help_text = """
Help Information for eems setup.
Usage:
  eems-server <command>
Commands:
  install             Install eems server.
  uninstall           Uninstall eems server.
  -h --help           Show help.
"""


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def main(setup_path):
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
        print 'install'
        file_path = '{}/setup.sh'.format(setup_path)
        # file_path = '/data/F_Projects/F-I_GitHub/eems/eems/scripts/install.sh'
        p = subprocess.Popen([file_path],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out

    elif args.command == 'uninstall':
        print 'uninstall'
        file_path = '{}/setup.sh'.format(setup_path)
        # file_path = '/data/F_Projects/F-I_GitHub/eems/eems/scripts/install.sh'
        p = subprocess.Popen([file_path],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out

    else:
        print help_text


if __name__ == '__main__':
    main(path)
