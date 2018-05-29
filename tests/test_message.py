from chat_messages.message import Message

import unittest


class TestMessage(unittest.TestCase):
    """
    Test case for class Message
    """

    def test_message_text(self):
        """
        Test to check if the text given as input as stored as an attribute
        """
        test_message = 'hey! what are you doing?'
        message = Message(text=test_message)

        self.assertEqual(message._text, test_message)


if __name__ == '__main__':
    unittest.main()