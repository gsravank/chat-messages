from chat_messages.config import TEXT_COL

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class Plots(object):
    """
    Class to represent all plots to go in the final image.
    """

    def __init__(self, report_p1, report_p2, font_size=20):
        """
        Constructor to get dataframes of messages, colors of plots, etc.
        """
        self._p1_report = report_p1
        self._p2_report = report_p2
        self._font_size = font_size

        # Set font size
        mpl.rcParams['font.size'] = 20.0

        # Get names for labels in plots
        self._names = [report_p1.get_name(), report_p2.get_name()]

    @staticmethod
    def pie_chart(figsize, values, labels, title, save_file=None, display_plot=False):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1, 1, 1)
        ax.pie(values, startangle=90, labels=labels, autopct='%1.1f%%',)
        plt.title(title)

        if display_plot:
            plt.show()

        if save_file:
            fig.savefig(save_file, bbox_inches='tight')

    @staticmethod
    def side_by_side_bar_chart(num_values, width, figsize, values_one, values_two, title, labels, xtick_pos, xtick_labels, display_plot=False, save_file=None):
        ind = np.arange(num_values)

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        rects1 = ax.bar(ind, values_one, width)
        rects2 = ax.bar(ind + width, values_two, width)

        ax.set_title(title)
        ax.set_xticks(xtick_pos)
        ax.set_xticklabels(xtick_labels)
        ax.legend((rects1[0], rects2[0]), labels)

        if display_plot:
            plt.show()

        if save_file:
            fig.savefig(save_file)

    def pie_chart_num_messages(self, file_path=None, display_plot=False):
        figsize = (8, 8)
        values = [len(self._p1_report.get_messages()), len(self._p2_report.get_messages())]
        labels = self._names
        title = 'Number of Messages Sent'

        self.pie_chart(figsize, values, labels, title, save_file=file_path, display_plot=display_plot)

    def pie_chart_num_words(self, file_path=None, display_plot=False):
        figsize = (8, 8)
        values = [len(self._p1_report.get_words()), len(self._p2_report.get_words())]
        labels = self._names
        title = 'Number of Words Sent'

        self.pie_chart(figsize, values, labels, title, save_file=file_path, display_plot=display_plot)

    def bar_chart_messages_by_weekday(self, file_path=None, display_plot=False):
        num_values = 7
        width = 0.35
        figsize = (10, 8)
        ind = width + np.arange(num_values)

        values_one = self._p1_report.get_messages_by_weekday().reindex([3, 1, 5, 6, 4, 0, 2])[TEXT_COL].tolist()
        values_two = self._p2_report.get_messages_by_weekday().reindex([3, 1, 5, 6, 4, 0, 2])[TEXT_COL].tolist()

        title = 'Messages by Weekday'
        labels = self._names

        xtick_pos = ( ind + width / 2)
        xtick_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        self.side_by_side_bar_chart(num_values, width, figsize, values_one, values_two, title, labels, xtick_pos, xtick_labels, display_plot=display_plot, save_file=file_path)

    def bar_chart_messages_by_month(self, file_path=None, display_plot=False):
        num_values = 12
        width = 0.35
        figsize = (10, 8)
        ind = width + np.arange(num_values)

        values_one = self._p1_report.get_messages_by_month()[TEXT_COL].tolist()
        values_two = self._p2_report.get_messages_by_month()[TEXT_COL].tolist()

        title = 'Messages by Month'
        labels = self._names

        xtick_pos = ( ind + width/2 )
        xtick_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        self.side_by_side_bar_chart(num_values, width, figsize, values_one, values_two, title, labels, xtick_pos,
                                    xtick_labels, display_plot=display_plot, save_file=file_path)

    def bar_chart_messages_by_hour(self, file_path=None, display_plot=False):
        num_values = 24
        width = 0.30
        figsize = (14, 12)
        ind = width + np.arange(num_values)

        values_one = self._p1_report.get_messages_by_hour_of_day()[TEXT_COL].tolist()
        values_two = self._p2_report.get_messages_by_hour_of_day()[TEXT_COL].tolist()

        title = 'Messages by Hour of Day'
        labels = self._names

        xtick_pos = ( ind + width/2)
        xtick_labels = range(24)

        self.side_by_side_bar_chart(num_values, width, figsize, values_one, values_two, title, labels, xtick_pos,
                                    xtick_labels, display_plot=display_plot, save_file=file_path)
