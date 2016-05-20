# -*- coding: utf-8 -*-
"""
Others module provides additional functions.
"""


import os
import subprocess


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


def set_permissions(user):
    """Public function *set_permissions* sets the permissions of the directory
        */home/$USER/eems* to *$USER:$USER*. *$USER* will be replaced with the actual user's name.
        Requires *sudo*!

    :return:
        Returns *None*.
    """
    args = ['sudo', 'chown', '-cR', '{}:{}'.format(user, user), '/var/www/eems']
    subprocess.Popen(args)
