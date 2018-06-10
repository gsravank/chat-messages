from chat_messages.config import PROCESSED_MESSAGES_PATH, CSV_SEP, REPORT_START_DATE, REPORT_END_DATE, DATETIME_COL, TEXT_COL

import pandas as pd
from dateutil import parser
from collections import Counter
import operator
import emoji
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


mpl.rcParams['font.size'] = 20.0


def get_messages_dataframe(messages_file_path, separator, start_date, end_date):
    messages = pd.read_csv(messages_file_path, separator)
    messages[DATETIME_COL] = messages[DATETIME_COL].apply(lambda date_str: parser.parse(date_str))

    messages = messages[(messages[DATETIME_COL] >= start_date) & (messages[DATETIME_COL] <= end_date)]

    return messages[['sender', 'datetime', 'processed_text']]


def get_messages_df_by_sender(messages_df, sender):
    return messages_df[messages_df['sender'] == sender]


class Report(object):
    """
    Class to maintain messages dataframe of a person and report relevant statistics.
    """

    def __init__(self, messages_df, sender):
        """
        Constructor to read pandas dataframe of messages sent by a person

        Args:
            messages_df (pd.DataFrame): Dataframe of messages and timestamps by a person
            sender (str): Name of the sender
        """
        self._messages_df = messages_df
        self._sender = sender
        self._messages = self.get_messages()
        self._words = self.get_words()

    def get_name(self):
        return self._sender

    def get_messages(self):
        """
        Get list of messages sent by the person.

        Returns:
            list of str: List of all messages sent by the person

        """
        return self._messages_df[TEXT_COL].tolist()

    def get_words(self):
        """
        Get concatenated list of all words in all messages sent by the person.

        Returns:
            list of str: List of all words in all messages
        """
        words = list()

        for message in self._messages:
            message_words = str(message).split(' ')
            words.extend(message_words)

        return words

    def get_words_per_message(self):
        """
        Return average words per message.

        Returns:
            float: Average length of a message
        """
        lengths_of_messages = [len(str(message).split(' ')) for message in self._messages]

        return float(sum(lengths_of_messages)) / len(self._messages)

    def get_number_of_pictures_sent(self):
        """
        Return total number of images sent by person.

        Returns:
            int: Total number of messages which were images
        """
        photo_messages = [message for message in self._messages if str(message).strip() == '[[photo]]']

        return len(photo_messages)

    def get_frequent_words(self):
        """
        Get most frequent words used by the person.

        Returns:
            list of tuples: Sorted list of words and frequencies in descending order
        """
        word_counts = Counter(self._words)
        sorted_word_counts = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)

        return sorted_word_counts

    def get_messages_by_weekday(self):
        """
        Get number of messages sent by weekday.

        Returns:
            pd.DataFrame: DataFrame with columns as weekdays and number of messages sent
        """
        self._messages_df['weekday'] = self._messages_df[DATETIME_COL].apply(lambda dt: dt.strftime("%A"))

        return self._messages_df.groupby('weekday')[TEXT_COL].count().reset_index()

    def get_messages_by_date(self):
        """
        Get number of messages sent by date.

        Returns:
            pd.DataFrame: DataFrame with columns as dates and number of messages sent
        """
        self._messages_df['date'] = self._messages_df[DATETIME_COL].apply(lambda dt: dt.strftime("%Y-%m-%d"))

        return self._messages_df.groupby('date')[TEXT_COL].count().reset_index()

    def get_messages_by_month(self):
        """
        Get number of messages sent by month.

        Returns:
            pd.DataFrame: DataFrame with columns as months and number of messages sent
        """
        self._messages_df['month'] = self._messages_df[DATETIME_COL].apply(lambda dt: dt.strftime("%Y-%m"))

        return self._messages_df.groupby('month')[TEXT_COL].count().reset_index()

    def get_messages_by_hour_of_day(self):
        """
        Get number of messages sent by hour of day.

        Returns:
            pd.DataFrame: DataFrame with columns as hour of day and number of messages sent
        """
        self._messages_df['hour'] = self._messages_df[DATETIME_COL].apply(lambda dt: dt.strftime("%H"))

        return self._messages_df.groupby('hour')[TEXT_COL].count().reset_index()

    def get_frequent_emojis(self):
        """
        Get most frequent words used by the person.

        Returns:
            list of tuples: Sorted list of words and frequencies in descending order
        """
        emojis = [word for word in self._words if word in emoji.UNICODE_EMOJI]
        emoji_counts = Counter(emojis)
        sorted_emoji_counts = sorted(emoji_counts.items(), key=operator.itemgetter(1), reverse=True)

        return sorted_emoji_counts

    def get_most_active_day(self):
        date_messages = self.get_messages_by_date()
        max_date_message_count = max(date_messages[TEXT_COL].tolist())

        max_date_rows = date_messages[date_messages[TEXT_COL] == max_date_message_count]
        return max_date_rows.iloc[0]['date']

    def get_messages_on_day(self, date_str):
        """
        Get dataframe of messages on a particular date.

        Args:
            date_str (str): Date in 'YYYY-MM-DD' format

        Returns:
            pd.DataFrame: Table of messages on a particular date
        """
        return self._messages_df[self._messages_df['date'] == date_str][[DATETIME_COL, TEXT_COL]]


def main():
    messages_df = get_messages_dataframe(PROCESSED_MESSAGES_PATH, CSV_SEP, REPORT_START_DATE, REPORT_END_DATE)
    print(messages_df.head())

    sravan_messages_df = messages_df[messages_df['sender'] == 'Sravan']
    sravan_report = Report(sravan_messages_df, 'Sravan')

    harsha_messages_df = messages_df[messages_df['sender'] == 'Harsha']
    harsha_report = Report(harsha_messages_df, 'Harsha')
    print('\n' + '=' * 80 + '\n')

    # Total Messages sent
    print('Messages sent by Sravan: {}'.format(len(sravan_report.get_messages())))
    print('Messages sent by Harsha: {}'.format(len(harsha_report.get_messages())))
    print('Total messages sent between {} and {}: {}'.format(REPORT_START_DATE, REPORT_END_DATE, len(messages_df)))
    print('\n' + '='*80 + '\n')
    # fig = plt.figure(figsize=(8, 8))
    # ax = fig.add_subplot(1, 1, 1)
    # ax.pie([len(sravan_report.get_messages()), len(harsha_report.get_messages())], startangle=90, labels=['Sravan', 'Harsha'], autopct='%1.1f%%',)
    # plt.title('Number of messages sent', fontsize=20)
    # plt.show()
    # fig.savefig('images/number_of_messages_sent_pie.png', bbox_inches='tight')

    # Words per message
    print('Words per message for Sravan: {}'.format(sravan_report.get_words_per_message()))
    print('Total number of words sent by Sravan: {}\n'.format(len(sravan_report.get_words())))

    print('Words per message for Harsha: {}'.format(harsha_report.get_words_per_message()))
    print('Total number of words sent by Harsha: {}'.format(len(harsha_report.get_words())))
    print('\n' + '=' * 80 + '\n')

    # Pictures sent
    print('Number of photos sent by Sravan: {}'.format(sravan_report.get_number_of_pictures_sent()))
    print('Number of photos sent by Harsha: {}'.format(harsha_report.get_number_of_pictures_sent()))
    print('\n' + '=' * 80 + '\n')

    # Most used words
    print('Top words used by Sravan:\n')
    sravan_total_num_words = len(sravan_report.get_words())
    for word, count in sravan_report.get_frequent_words()[:16]:
        if word[:2] != '[[':
            print('{} - {:02.1f}%'.format(word, 100.0 * float(count)/sravan_total_num_words))
    print('\n')

    print('Top words used by Harsha:\n')
    harsha_total_num_words = len(harsha_report.get_words())
    for word, count in harsha_report.get_frequent_words()[:15]:
        print('{} - {:02.1f}%'.format(word, 100.0 * float(count)/harsha_total_num_words))
    print('\n' + '=' * 80 + '\n')


    # Number of messages by weekday
    print('Sravan messages by weekday: \n')
    sravan_messages_by_weekday = sravan_report.get_messages_by_weekday().reindex([3, 1, 5, 6, 4, 0, 2])
    print(sravan_messages_by_weekday)
    print('\nHarsha messages by weekday: \n')
    harsha_messages_by_weekday = harsha_report.get_messages_by_weekday().reindex([3, 1, 5, 6, 4, 0, 2])
    print(harsha_messages_by_weekday)
    print('\n' + '=' * 80 + '\n')

    # N = 7
    # ind = np.arange(N)
    # width = 0.35
    #
    # fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111)
    # rects1 = ax.bar(ind, sravan_messages_by_weekday[TEXT_COL].tolist(), width)
    # rects2 = ax.bar(ind + width, harsha_messages_by_weekday[TEXT_COL].tolist(), width)
    #
    # ax.set_title('Messages by Weekday')
    # ax.set_xticks(ind + width / 2)
    # ax.set_xticklabels([x[:3] for x in sravan_messages_by_weekday['weekday'].tolist()])
    # ax.legend((rects1[0], rects2[0]), ('Sravan', 'Harsha'))
    #
    # plt.show()
    # fig.savefig('images/messages_by_weekday_bar.png')


    # Messages by day
    print('Sravan messages by day: \n')
    sravan_messages_by_date = sravan_report.get_messages_by_date()
    print(sravan_messages_by_date.head())
    print('\nHarsha messages by day: \n')
    harsha_messages_by_date = harsha_report.get_messages_by_date()
    print(harsha_messages_by_date.head())
    print('\n' + '=' * 80 + '\n')

    # N = len(sravan_messages_by_date)
    # ind = np.arange(N)
    # width = 0.1
    #
    # fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111)
    # rects1 = ax.bar(ind, sravan_messages_by_date[TEXT_COL].tolist(), width)
    # rects2 = ax.bar(ind + width, harsha_messages_by_date[TEXT_COL].tolist(), width)
    #
    # ax.set_title('Messages Sent Over the Year')
    # ax.set_xticks(ind + width / 2)
    # # ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    # ax.legend((rects1[0], rects2[0]), ('Sravan', 'Harsha'))
    #
    # plt.show()
    # fig.savefig('images/messages_by_month_bar.png')

    # Messages by month

    print('Sravan messages by month: \n')
    sravan_messages_by_month = sravan_report.get_messages_by_month()
    print(sravan_messages_by_month)
    print('\nHarsha messages by month: \n')
    harsha_messages_by_month = harsha_report.get_messages_by_month()
    print(harsha_messages_by_month)
    print('\n' + '=' * 80 + '\n')

    # N = 12
    # ind = np.arange(N)
    # width = 0.35
    #
    # fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111)
    # rects1 = ax.bar(ind, sravan_messages_by_month[TEXT_COL].tolist(), width)
    # rects2 = ax.bar(ind + width, harsha_messages_by_month[TEXT_COL].tolist(), width)
    #
    # ax.set_title('Messages by Month')
    # ax.set_xticks(ind + width / 2)
    # ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    # ax.legend((rects1[0], rects2[0]), ('Sravan', 'Harsha'))
    #
    # plt.show()
    # fig.savefig('images/messages_by_month_bar.png')

    # Messages by hour of day

    print('Sravan messages by hour: \n')
    sravan_messages_by_hour = sravan_report.get_messages_by_hour_of_day()
    print(sravan_messages_by_hour)
    print('\nHarsha messages by hour: \n')
    harsha_messages_by_hour = harsha_report.get_messages_by_hour_of_day()
    print(harsha_messages_by_hour)
    print('\n' + '=' * 80 + '\n')

    # N = 24
    # ind = np.arange(N)
    # width = 0.30
    #
    # fig = plt.figure(figsize=(14, 12))
    # ax = fig.add_subplot(111)
    # rects1 = ax.bar(ind, sravan_messages_by_hour[TEXT_COL].tolist(), width)
    # rects2 = ax.bar(ind + width, harsha_messages_by_hour[TEXT_COL].tolist(), width)
    #
    # ax.set_title('Messages by Hour of Day')
    # ax.set_xticks(ind + width / 2)
    # ax.set_xticklabels(sravan_messages_by_hour['hour'].tolist())
    # ax.legend((rects1[0], rects2[0]), ('Sravan', 'Harsha'))
    #
    # plt.show()
    # fig.savefig('images/messages_by_hour_bar.png')

    # Most frequent emojis

    print('Sravans top emojis:\n')
    for emoj, count in sravan_report.get_frequent_emojis()[:10]:
        print("{}: {}".format(emoj, count))
    print('\n\nHarshas top emojis: \n')
    harsha_emojis = list()
    harsha_emoji_counts = list()

    for emoj, count in harsha_report.get_frequent_emojis()[:10]:
        print("{}: {}".format(emoj, count))
        harsha_emojis.append("{}".format(emoji))
        harsha_emoji_counts.append(count)
    print('\n' + '=' * 80 + '\n')

    print(harsha_emojis)
    print(harsha_emoji_counts)

    num_values = 10
    ind = np.arange(num_values)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    values_one = harsha_emoji_counts
    rects1 = ax.bar(ind, values_one, 0.4, color='#ff7f0e')

    ax.set_title("Harsha's Frequent Emojis")
    # ax.set_xticks(['' for _ in range(num_values)])
    fig.savefig('images/harsha_emojis_bar.png')

    # Most active day
    print(sravan_report.get_most_active_day())
    print(harsha_report.get_most_active_day())

    # Messages on most active day
    print(sravan_report.get_messages_on_day(sravan_report.get_most_active_day()))
    print(harsha_report.get_messages_on_day(harsha_report.get_most_active_day()))


    return


if __name__ == '__main__':
    main()