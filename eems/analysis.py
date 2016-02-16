# -*- coding: utf-8 -*-


import pandas


def analysis():
    print 'statistische auswertung'


def import_data(csv_file):
    content = pandas.read_csv(filepath_or_buffer=csv_file, sep=';')
    return content
