from chat_messages.config import ORIGINAL_MESSAGES_PATH, PROCESSED_MESSAGES_PATH

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

    for message in messages:
        try:
            # Get date
            time = message[:19]
            datetime_obj = parse(time)

            remaining_line = message[21:]

            # Get user name
            for idx, char in enumerate(remaining_line):
                if char == ':':
                    colon_idx =  idx
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
        except Exception:
            pass

    final_df = pd.DataFrame({'time': message_times, 'sender': senders, 'text': message_texts})
    final_df = final_df[['time', 'sender', 'text']]

    return final_df


def main():
    # Get a list of messages. Stick new lines to previous message
    messages = get_messages()

    # Get message dataframe
    messages_df = get_message_details(messages)
    print('\n\n')
    print(messages_df[100:200])

    # s = messages_df.iloc[101]['text']
    # print(s)
    # print(len(s))
    # print(type(s))
    # print(s.isalpha())
    # print(bytes(s, encoding='utf-8'))
    # print(len(bytes(s, encoding='utf-8')))


    return


if __name__ == '__main__':
    main()