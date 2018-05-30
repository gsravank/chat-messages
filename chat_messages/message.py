"""
Module which contains definition for message class.

This module contains Message class which takes in the message and assigns to each instance the
text, time and other details related to the message text.
"""


class Message(object):
    """
    Class to represent each text message sent by any person

    Attributes:
        text (str): The processed/original message text

    """

    def __init__(self, text, sender, time):
        """
        Constructor to initialise the message details

        Args:
             text (str): The processed/original text message
        """
        self._text = text
        self._sender = sender
        self._time = time