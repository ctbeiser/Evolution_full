from main import generate_score_string
from unittest import TestCase


class MainTestCase(TestCase):

    def test_generating_score(self):
        example = []
        self.assertEqual(generate_score_string([]), "")
        example.append((0, 777, "Hello!"))
        self.assertEqual(generate_score_string(example), "1 player id: 777 score: 0 handshake: Hello!\n")
        example.append((345, 773, "Y"))
        self.assertEqual(generate_score_string(example), "1 player id: 777 score: 0 handshake: Hello!\n2 player "
                                                         + "id: 773 score: 345 handshake: Y\n")