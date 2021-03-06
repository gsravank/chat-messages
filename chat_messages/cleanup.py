from chat_messages.config import ORIGINAL_MESSAGES_PATH, PROCESSED_MESSAGES_PATH, CSV_SEP
from chat_messages.text_utils import identify_forwards, identify_links, identify_special_texts, separate_emojis_at_the_end_of_tokens, convert_smileys_to_emojis, separate_special_characters_at_the_end_of_tokens


from dateutil.parser import parse
import pandas as pd


def starts_with_date(line):
    first_ten_chars = line[:10]

    try:
        parse(first_ten_chars)
        return True
    except Exception:
        return False


def get_messages():
    with open(ORIGINAL_MESSAGES_PATH, 'r') as f:
        lines = f.readlines()

    messages = list()

    for line in lines:
        if starts_with_date(line):
            messages.append(line)
        else:
            prev_message = messages.pop()
            prev_message += line
            messages.append(prev_message)

    return messages


def get_message_details(messages):
    message_times = list()
    senders = list()
    message_texts = list()
    datetimes = list()

    for message in messages:
        try:
            # Get date
            time = message[:19]

            # Change to mm.dd.yyyy format
            new_time = time[3:5] + '.' + time[:2] + time[5:]
            datetime_obj = parse(new_time)

            remaining_line = message[21:]

            # Get user name
            for idx, char in enumerate(remaining_line):
                if char == ':':
                    colon_idx = idx
                    break

            user_text = remaining_line[:colon_idx]
            remaining_line = remaining_line[colon_idx + 2:]

            if 'Sravan' in user_text:
                sender = 'Sravan'
            else:
                sender = 'Harsha'

            # Get actual text
            text = remaining_line.strip()

            message_times.append(time)
            senders.append(sender)
            message_texts.append(text)
            datetimes.append(datetime_obj)
        except Exception:
            pass

    final_df = pd.DataFrame({'time': message_times, 'sender': senders, 'text': message_texts, 'datetime': datetimes})
    final_df = final_df[['time', 'sender', 'text', 'datetime']]

    return final_df


def get_time_details(messages_df):
    # Get year, month, date, hour, min, sec, weekday from datetime object
    messages_df['year'] = messages_df['datetime'].apply(lambda dt: dt.year)
    messages_df['month'] = messages_df['datetime'].apply(lambda dt: dt.month)
    messages_df['date'] = messages_df['datetime'].apply(lambda dt: dt.day)
    messages_df['hour'] = messages_df['datetime'].apply(lambda dt: dt.hour)
    messages_df['minute'] = messages_df['datetime'].apply(lambda dt: dt.minute)
    messages_df['second'] = messages_df['datetime'].apply(lambda dt: dt.second)
    messages_df['weekday'] = messages_df['datetime'].apply(lambda dt: dt.strftime("%A"))

    return messages_df


def process_text_message(text):
    # Lower
    text = text.lower()

    # # Check if message is not a regular text
    # if_forward = identify_forwards(text)
    # if_link = identify_links(text)
    # special_text = identify_special_texts(text)
    #
    # if if_forward:
    #     text = '[[FWD]]'
    # elif if_link:
    #     text = '[[LINK]]'
    # elif special_text:
    #     text = special_text
    # else:

    # Separate emojis at the end of words
    text = separate_emojis_at_the_end_of_tokens(text)

    # Separate special characters at the end of words
    text = separate_special_characters_at_the_end_of_tokens(text)

    # Convert smileys to emojis
    text = convert_smileys_to_emojis(text)

    return text


def get_processed_text(messages_df):
    messages_df['processed_text'] = messages_df['text'].apply(lambda text: process_text_message(text))

    return messages_df


def main():
    # Get a list of messages. Stick new lines to previous message
    messages = get_messages()

    # Get message dataframe
    messages_df = get_message_details(messages)

    # Get time related details
    messages_df = get_time_details(messages_df)

    # Process text message
    messages_df = get_processed_text(messages_df)
    messages_df.to_csv(PROCESSED_MESSAGES_PATH, CSV_SEP)

    print(messages_df.head(100))

    return


if __name__ == '__main__':
    main()