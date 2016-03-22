# -*- coding: utf-8 -*-
"""
This module shell includes functions interacting with the shell.
"""


import subprocess


def set_permissions():
    """Public function *set_permissions* sets the permissions of the directory
        */home/pi/eems* to *pi:pi*. Requires *sudo*.

    :return:
        Returns *None*.
    """
    args = ['sudo', 'chown', '-cR', 'pi:pi', '/home/pi/eems']
    subprocess.Popen(args)
