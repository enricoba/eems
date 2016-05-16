# -*- coding: utf-8 -*-
"""
This module shell includes functions interacting with the shell.
"""


import subprocess
import getpass


def set_permissions():
    """Public function *set_permissions* sets the permissions of the directory
        */home/$USER/eems* to *$USER:$USER*. *$USER* will be replaced with the actual user's name.
        Requires *sudo*!

    :return:
        Returns *None*.
    """
    user = getpass.getuser()
    args = ['sudo', 'chown', '-cR', '{}:{}'.format(user, user), '/home/{}/eems'.format(user)]
    subprocess.Popen(args)
