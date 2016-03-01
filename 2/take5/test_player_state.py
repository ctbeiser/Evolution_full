from unittest import TestCase
from unittest.mock import MagicMock

from dummy_player import DummyPlayer
from definitions import Card
from player_state import PlayerState


class TestPlayerState(TestCase):

    def setUp(self):
        self.player = DummyPlayer(0, 1)
        self.stacks = (
            [Card(2, 2)],
            [Card(3, 2)],
            [Card(4, 2)],
            [Card(5, 2)],
        )

    def test_set_cards(self):

        cards = [Card(1, 1)]
        ps = PlayerState(self.player)

        self.assertEqual(ps.cards, None)
        ps.set_cards(cards)
        self.assertEqual(ps.cards, cards)

    def test_choose_card(self):

        cards = [Card(1, 1)]

        ps = PlayerState(self.player)
        ps.set_cards(cards)

        # dummy player always chooses first card
        self.assertEqual(ps.choose_card(self.stacks), cards[0])

    def test_choose_stack(self):

        ps = PlayerState(self.player)
        # dummy player always chooses first stack
        self.assertEqual(ps.choose_stack(self.stacks), 0)

    def test_stacks_updated(self):

        ps = PlayerState(self.player)
        ps.player.on_stacks_updated = MagicMock()

        ps.stacks_updated(self.stacks)
        ps.player.on_stacks_updated.assert_called_once_with(self.stacks)

    def test_cards_chosen(self):

        cards = [Card(1, 2), Card(3, 4)]
        ps = PlayerState(self.player)
        ps.player.on_cards_chosen = MagicMock()

        ps.cards_chosen(cards)
        ps.player.on_cards_chosen.assert_called_once_with(cards)

