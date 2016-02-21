# -*- coding: utf-8 -*-


import numpy as np


def analysis(content):
    return np.mean(content)


def import_data(csv_file):
    if isinstance(csv_file, basestring) is True:
        content = np.genfromtxt(csv_file, delimiter=';', skip_header=True)
        return content

