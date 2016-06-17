# -*- coding: utf-8 -*-
"""
Script file for eems.
"""


import os
import sys
import argparse
import subprocess

from eems.support.database import init_db, db_session
from eems.support.models import General


help_text = """Help Information for eems setup.
Usage:
  eems-server <command>
Commands:
  setup               Set up eems server.
  uninstall           Uninstall eems server.
  -h --help           Show help."""


def get_user():
    """Public function *get_user* determines the actual user name.

    :return:
        Returns *string*.
    """
    sudo_user = os.getenv("SUDO_USER")
    if sudo_user is None:
        actual_user = os.getenv("USER")
    else:
        actual_user = sudo_user
    return actual_user


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
        actual_user = get_user()

        init_db()
        user = General('USER', actual_user)
        home = General('HOME', '/home/{}/eems'.format(actual_user))
        db_session.add_all(user, home)
        db_session.commit()
        db_session.remove()

        # subprocess.call([file_path, actual_user])
    elif args.command == 'uninstall':
        actual_user = get_user()
        file_path = '{}/uninstall.sh'.format(path)
        subprocess.call([file_path, actual_user])

    else:
        print help_text


if __name__ == '__main__':
    main()
