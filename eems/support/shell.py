# -*- coding: utf-8 -*-
"""
This module shell includes functions interacting with the shell.
"""


import subprocess


def set_permissions():
    args = ['sudo', 'chown', '-cR', 'pi:pi', '/home/pi/eems']
    subprocess.Popen(args)
