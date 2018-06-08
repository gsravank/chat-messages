from chat_messages.config import PROCESSED_MESSAGES_PATH, CSV_SEP, REPORT_START_DATE, REPORT_END_DATE, DATETIME_COL, TEXT_COL
from chat_messages.report import Report
from chat_messages.plots import Plots

import pandas as pd
from dateutil import parser


def get_messages_dataframe(messages_file_path, separator, start_date, end_date):
    messages = pd.read_csv(messages_file_path, separator)
    messages[DATETIME_COL] = messages[DATETIME_COL].apply(lambda date_str: parser.parse(date_str))

    messages = messages[(messages[DATETIME_COL] >= start_date) & (messages[DATETIME_COL] <= end_date)]

    return messages[['sender', 'datetime', 'processed_text']]


def get_messages_df_by_sender(messages_df, sender):
    return messages_df[messages_df['sender'] == sender]


def main():
    messages_df = get_messages_dataframe(PROCESSED_MESSAGES_PATH, CSV_SEP, REPORT_START_DATE, REPORT_END_DATE)

    sravan_messages_df = messages_df[messages_df['sender'] == 'Sravan']
    sravan_report = Report(sravan_messages_df, 'Sravan')

    harsha_messages_df = messages_df[messages_df['sender'] == 'Harsha']
    harsha_report = Report(harsha_messages_df, 'Harsha')

    plot_obj = Plots(harsha_report, sravan_report)

    # Pie Charts
    plot_obj.pie_chart_num_messages(display_plot=True)
    plot_obj.pie_chart_num_words(display_plot=True)

    # Side by side bar charts
    plot_obj.bar_chart_messages_by_month(display_plot=True)
    plot_obj.bar_chart_messages_by_weekday(display_plot=True)
    plot_obj.bar_chart_messages_by_hour(display_plot=True)

    return


if __name__ == '__main__':
    main()