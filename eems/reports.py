# -*- coding: utf-8 -*-


import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator


def summary():
    print ' '
    # TODO: Projektdaten + Kopfzeile


class ConvertingData(object):  #TODO: oder wird das schon in analysis gemacht?
    def __init__(self):
        self.date_format = '%Y-%m-%d %H:%M:%S'

    def str_time2date_time(self, str_date, str_time):
        date_time = str_date + ' ' + str_time

        timestamp = []

        for i in date_time:
            time_converter = time.strptime(i, self.date_format)
            dt = datetime.datetime.fromtimestamp(time.mktime(time_converter))
            timestamp.append(dt)
        return np.array(timestamp)

    def timestamp2date_time(self, timestamp):
        new_time = datetime.datetime.fromtimestamp(int(timestamp)).strftime(self.date_format)
        return new_time


class Plotting(object):
    def __init__(self, data):
        # TODO: einstell möglichkeiten vom Nutzer festlegen
        self.converter = ConvertingData()
        self.data = data  # TODO: Stuktur überprüfen bzw. festlegen
        self.date_plot_format = '%Y-%m-%d %H:%M'  # TODO: Darstellung vom Timestamp klären
        self.line_width = 3
        self.line_style = '-'
        # TODO: Farben für Diagramme festlegen

    def plot_all(self, save=False):
        fig, ax = plt.subplots()
        fig.set_size_inches(11.8, 8.5, forward=True)  # TODO: Diagramm größe festlegen
        fig.set_tight_layout(True)
        for name in self.data.dtype.names:
            ax.plot(self.converter.str_time2date_time(str_date=self.data['Date'],
                                                      str_time=self.data['Time']),
                    self.data[name],
                    lw=self.line_width,
                    ls=self.line_style,
                    label=name)  # TODO: Label zuweisung klären

        # graphic options
        date_format = mdates.DateFormatter(self.date_plot_format)
        rule = mdates.rrulewrapper(mdates.HOURLY, interval=2)  # TODO: Darstellungsintervall für major-grid festlegen
        loc = mdates.RRuleLocator(rule)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        ax.grid(True, 'major')

        # Minor Grid
        rule_minor = mdates.rrulewrapper(mdates.MINUTELY, interval=2)
        loc_minor = mdates.RRuleLocator(rule_minor)
        ax.xaxis.set_minor_locator(loc_minor)
        ax.yaxis.set_minor_locator(MultipleLocator(0.02))
        ax.grid(True, 'minor')

        # Labels
        ax.set_ylabel(u'Temperature in °C')
        ax.set_xlabel(u'Time')

        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        ax.legend(handles, labels, fontsize=11, ncol=3, loc='best')

        if save is True:
            filename = '.jpg'  # TODO: filename
            fig.savefig(filename, dpi=300)
        plt.show()

    def plot_only(self, save=False):
        for name in self.data.dtype.names:
            fig, ax = plt.subplots()
            fig.set_size_inches(11.8, 8.5, forward=True)   # TODO: Diagramm größe festlegen
            fig.set_tight_layout(True)
            ax.plot(self.converter.str_time2date_time(str_date=self.data['Date'],
                                                      str_time=self.data['Time']),
                    self.data[name],
                    lw=self.line_width,
                    ls=self.line_style,
                    label=name)  # TODO: Label zuweisung klären

            # graphic options
            date_format = mdates.DateFormatter(self.date_plot_format)
            rule = mdates.rrulewrapper(mdates.HOURLY, interval=2)  # TODO: Darstellungsintervall festlegen
            loc = mdates.RRuleLocator(rule)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(date_format)
            fig.autofmt_xdate()
            ax.grid(True, 'major')

            # Minor Grid
            rule_minor = mdates.rrulewrapper(mdates.MINUTELY, interval=2)  # TODO: Darstellungsintervall festlegen
            loc_minor = mdates.RRuleLocator(rule_minor)
            ax.xaxis.set_minor_locator(loc_minor)
            ax.yaxis.set_minor_locator(MultipleLocator(0.02))  # TODO: Darstellungsintervall
            ax.grid(True, 'minor')

            ax.set_ylabel(u'Temperature in °C')
            ax.set_xlabel(u'Time')

            plt.legend(loc='best', fontsize=11, ncol=3)
            if save is True:
                filename = '.jpg'  # TODO: filename
                fig.savefig(filename, dpi=300)
        plt.show()


class PdfExport(object):  # TODO: oder als Funktion
    def __init__(self):
        print ' '
