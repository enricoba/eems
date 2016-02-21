# -*- coding: utf-8 -*-


import time
import numpy as np


def analysis(content):
    return np.mean(content)


def import_data(csv_file, sensor_count):
    with open(csv_file, 'rb') as csv:
        header = csv.readlines()[0].split(';')
    data_types_base = [int, time.struct_time, time.struct_time]
    data_types_sensors = sensor_count * [float]
    data_types = data_types_base + data_types_sensors
    content = np.genfromtxt(csv_file, delimiter=';', names=header,
                            skip_header=True, dtype=data_types)
    return content
