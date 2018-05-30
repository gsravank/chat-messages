"""
Module which contains class definition of a person.

This module contains the Person class which takes the name of the person and creates an instance with other details
related to this person.
"""


class Person(object):
    """
    Class to represent a person and details about him/her

    Attributes:
        name (str): Name of the person
    """

    def __init__(self, name):
        """
        Constructor to define the name and details of the person

        Args:
             name (str): Name of the person
        """
        self._name = name
