import unittest

from collections import namedtuple

from player import Player

Card = namedtuple("Card", "value bullvalue")


class TestPlayer(unittest.TestCase):

    def generate_stack(self, cards):
        return [Card(v, b) for v, b in cards]

    def setUp(self):
        self.player = Player(0, 0)

    def test_on_new_turn(self):

        card_hi = Card(10, 1)
        card_mi = Card(5, 1)
        card_lo = Card(1, 1)

        stacks = [self.generate_stack([(10, 1)])] * 4

        # highest is first
        hand1 = [card_hi, card_mi, card_lo]
        self.assertEqual(self.player.on_new_turn(hand1, stacks), card_hi)

        # highest is in the middle
        hand1 = [card_mi, card_hi, card_lo]
        self.assertEqual(self.player.on_new_turn(hand1, stacks), card_hi)

        # highest is last
        hand1 = [card_lo, card_mi, card_hi]
        self.assertEqual(self.player.on_new_turn(hand1, stacks), card_hi)

    def test_choose_stack_to_take(self):

        # first is lowest
        stacks = [
            self.generate_stack([(1, 1)]),
            self.generate_stack([(2, 2)]),
            self.generate_stack([(3, 3)]),
            self.generate_stack([(4, 4)]),
        ]

        self.assertEqual(self.player.choose_stack_to_take(stacks), 0)

        # sum is lowest
        stacks = [
            self.generate_stack([(2, 5)]),
            self.generate_stack([(1, 1), (10, 1)]),
            self.generate_stack([(3, 3)]),
            self.generate_stack([(4, 4)]),
        ]

        self.assertEqual(self.player.choose_stack_to_take(stacks), 1)


