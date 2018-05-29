from chat_messages.person import Person

import unittest


class TestPerson(unittest.TestCase):
    """
    Test case for the class Person
    """

    def test_person_name(self):
        """
        Test that the name given is stored as the name attribute
        """
        test_name = 'Albert Einstein'
        person = Person(name=test_name)

        self.assertEqual(person._name, test_name)


if __name__ == '__main__':
    unittest.main()