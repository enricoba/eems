# -*- coding: utf-8 -*-

import imports
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def summary():
    print ' '
    # TODO: Projektdaten + Kopfzeile


class Plotting(object):
    def __init__(self, data):
        # TODO: einstell möglichkeiten vom Nutzer festlegen
        self.data = data  # TODO: Stuktur überprüfen bzw. festlegen
        self.date_plot_format = '%Y-%m-%d %H:%M'  # TODO: Darstellung vom Timestamp klären
        self.line_width = 3
        self.line_style = '-'
        # TODO: Farben für Diagramme festlegen

        # TODO: Darstellungsintervall zentral festlegen
        x_skalierung = {'step_1': [mdates.HOURLY, 2, mdates.MINUTELY, 30],
                        'step_2': [mdates.HOURLY, 2, mdates.MINUTELY, 30]}
        self.x_major_steps = x_skalierung['step_1'][0]
        self.x_major_interval = x_skalierung['step_1'][1]
        self.x_minor_steps = x_skalierung['step_1'][2]
        self.x_minor_interval = x_skalierung['step_1'][3]

    def plot_all(self, save=False):
        fig, ax = plt.subplots()
        fig.set_size_inches(11.8, 8.5, forward=True)  # TODO: Diagramm größe festlegen
        fig.set_tight_layout(True)
        for name in self.data.dtype.names:
            ax.plot(self.data['timestamp'],
                    self.data[name],
                    lw=self.line_width,
                    ls=self.line_style,
                    label=name)

        # TODO: x-Achsenformatierung in funktion auslagern
        # graphic options
        date_format = mdates.DateFormatter(self.date_plot_format)
        rule = mdates.rrulewrapper(self.x_major_steps, interval=self.x_major_interval)
        loc = mdates.RRuleLocator(rule)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        ax.grid(True, 'major')

        # Minor Grid
        rule_minor = mdates.rrulewrapper(self.x_minor_steps, interval=self.x_minor_interval)
        loc_minor = mdates.RRuleLocator(rule_minor)
        ax.xaxis.set_minor_locator(loc_minor)
        ax.grid(True, 'minor')

        # Labels
        ax.set_ylabel(u'Temperature in °C')
        ax.set_xlabel(u'Time')
        ax.legend(fontsize=11, ncol=3, loc='best')

        if save is True:
            filename = '.jpg'  # TODO: filename
            fig.savefig(filename, dpi=300)
        plt.show()

    def plot_only(self, save=False):
        for name in self.data.dtype.names:
            fig, ax = plt.subplots()
            fig.set_size_inches(11.8, 8.5, forward=True)   # TODO: Diagramm größe festlegen
            fig.set_tight_layout(True)
            ax.plot(self.data['timestamp'],
                    self.data[name],
                    lw=self.line_width,
                    ls=self.line_style,
                    label=name)

            # graphic options
            date_format = mdates.DateFormatter(self.date_plot_format)
            rule = mdates.rrulewrapper(self.x_major_steps, interval=self.x_major_interval)
            loc = mdates.RRuleLocator(rule)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(date_format)
            fig.autofmt_xdate()
            ax.grid(True, 'major')

            # Minor Grid
            rule_minor = mdates.rrulewrapper(self.x_minor_steps, interval=self.x_minor_interval)
            loc_minor = mdates.RRuleLocator(rule_minor)
            ax.xaxis.set_minor_locator(loc_minor)
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
