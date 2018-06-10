from chat_messages.report import Report
from chat_messages.config import SENDER_COL
from chat_messages.plots import Plots

import os


class Image(object):
    """
    Class to take all plots and make into one final image.
    """
    def __init__(self, messages_df, person_one, person_two, image_dir='images'):
        self._image_dir = image_dir
        self._person_one_messages_df = messages_df[messages_df[SENDER_COL] == person_one]
        self._person_one_report = Report(self._person_one_messages_df, person_one)

        self._person_two_messages_df = messages_df[messages_df[SENDER_COL] == person_two]
        self._person_two_report = Report(self._person_two_messages_df, person_two)

        # Object to get all plots
        self._plot_obj = Plots(self._person_one_report, self._person_two_report)

    def draw_plots(self):
        file_names = ['number_of_messages_pie.png', 'number_of_words_pie.png', 'messages_by_month_bar.png', 'messages_by_weekday_bar.png', 'messages_by_hour_bar.png']
        full_file_names = [os.path.join(self._image_dir, file_name) for file_name in file_names]

        # Pie Charts
        self._plot_obj.pie_chart_num_messages(display_plot=True, file_path=full_file_names[0])
        self._plot_obj.pie_chart_num_words(display_plot=True, file_path=full_file_names[1])

        # Side by side bar charts
        self._plot_obj.bar_chart_messages_by_month(display_plot=True, file_path=full_file_names[2])
        self._plot_obj.bar_chart_messages_by_weekday(display_plot=True, file_path=full_file_names[3])
        self._plot_obj.bar_chart_messages_by_hour(display_plot=True, file_path=full_file_names[4])

        return full_file_names

    def draw_text(self, text):

        return