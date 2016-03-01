import unittest

from definitions import default_number_bullpoint_mapping, create_deck


class DefinitionsTests(unittest.TestCase):

    def test_default_number_bullpoint_mapping(self):

        test_cases = [
            (55, 7),
            (11, 5),
            (66, 5),
            (10, 3),
            (100, 3),
            (5, 2),
            (15, 2),
            (85, 2),
            (1, 1),
            (103, 1),
            (104, 1),
        ]

        for value, expected in test_cases:
            self.assertEqual(default_number_bullpoint_mapping(value), expected)

    def test_create_deck(self):

        deck = create_deck()
        self.assertEqual(len(deck), 104)
        self.assertEqual(len(set([card.value for card in deck])), 104)
