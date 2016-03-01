from unittest import TestCase

from dummy_player import DummyPlayer
from definitions import Card


card_1_2 = Card(1, 2)
card_3_4 = Card(3, 4)
card_10_20 = Card(10, 20)
card_11_21 = Card(11, 21)
card_12_22 = Card(12, 22)
card_13_23 = Card(13, 23)

stacks = ([card_10_20], [card_11_21], [card_12_22], [card_11_21])


class DummyPlayerTests(TestCase):

    def test_on_new_turn(self):

        hand = [card_1_2, card_3_4]
        player = DummyPlayer(0, 4)

        self.assertEqual(player.on_new_turn(hand, stacks), hand[0])

    def test_choose_stack_to_take(self):
        player = DummyPlayer(0, 4)
        self.assertEqual(player.choose_stack_to_take(stacks), 0)

    def test_on_cards_chosen(self):
        player = DummyPlayer(0, 4)
        self.assertEqual(player.on_cards_chosen([]), None)

    def test_on_stacks_updated(self):
        player = DummyPlayer(0, 4)
        self.assertEqual(player.on_stacks_updated(stacks), None)
