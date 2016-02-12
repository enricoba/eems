# -*- coding: utf-8 -*-


from numpy import genfromtxt


def analysis():
    print 'statistische auswertung'


def import_data(csv_file):
    content = genfromtxt(csv_file, delimiter=";", skip_header=1, dtype=None,
                         unpack=True)
    return content

