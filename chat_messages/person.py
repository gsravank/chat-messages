"""
Module which contains class definition of a person.

This module contains the Person class which takes the name and messages dataframe sent by a person
and calculates relevant statistics like number of messages sent, messages on specific weekdays, etc.
"""


class Person(object):
    """
    Class to represent a person and messages sent by him/her

    Attributes:
        name (str): Name of the person
    """
    def __init__(self, name):
        """
        Constructor to define the name and read list of messages sent by the person

        Args:
             name (str): Name of the person
             messages (list): List of message objects
        """
        self._name = name
