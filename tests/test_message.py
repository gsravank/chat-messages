from chat_messages.message import Message
from chat_messages.person import Person

import unittest
import datetime


class TestMessage(unittest.TestCase):
    """
    Test case for class Message
    """

    def test_message_text(self):
        """
        Test to check if the text, sender name and time given as input are stored as attributes
        """
        test_message = 'hey! what are you doing?'
        test_sender = Person('Einstein')
        test_time = datetime.datetime.now()
        message = Message(text=test_message, sender=test_sender, time=test_time)

        self.assertEqual(message._text, test_message)
        self.assertEqual(message._time, test_time)
        self.assertEqual(message._sender, test_sender)


if __name__ == '__main__':
    unittest.main()