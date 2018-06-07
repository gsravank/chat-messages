from dateutil import parser

# File Paths
ORIGINAL_MESSAGES_PATH = '/Users/sravan/Desktop/projects/chat-messages/chat_messages/data/telegram_messages.txt'
PROCESSED_MESSAGES_PATH = '/Users/sravan/Desktop/projects/chat-messages/chat_messages/data/processed_telegram_messages.csv'

# String Constants
CSV_SEP = '\x01'

# DataFrame Column Names
SENDER_COL = 'sender'
TEXT_COL = 'processed_text'
DATETIME_COL = 'datetime'

# Report Constants
REPORT_START_DATE = parser.parse('2017-01-01')
REPORT_END_DATE = parser.parse('2017-12-31')
