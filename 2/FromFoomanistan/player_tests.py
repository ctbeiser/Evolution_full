
import collections
import unittest

from player import Player


class TestPlayer(unittest.TestCase):
    """Test the 6Nimmt! Player implementation."""

    def setUp(self):
        self.player = Player(0, 4)
        self.discards = [self._make_card(43, 5),
                         self._make_card(44, 2),
                         self._make_card(45, 3),
                         self._make_card(46, 6)]
        self.stacks = ([self._make_card(47, 7)],
                       [self._make_card(48, 4)],
                       [self._make_card(49, 2)],
                       [self._make_card(50, 5)])

    def _make_card(self, value, bullvalue):
        """Makes a Card named tuple with the given value and bullvalue.

        @param value: int in [1, 104]
        @param bullvalue: int in [2, 7]
        @return: Card(value, bullvalue)
        """
        Card = collections.namedtuple('Card', ['value', 'bullvalue'])
        return Card(value, bullvalue)

    def _make_stacks(self, stack_values):
        """Makes a Stack with the given stack_values.

        @param stack_values: 4-tuple of list of (value, bullvalue) pairs.
        @return: A Stacks with the given stack_values. Each card in each stack
                 is specified by the corresponding tuple in stack_values.
        """
        return tuple([self._make_card(v, bv) for v, bv in stack]
                     for stack in stack_values)

    def test_init(self):
        self.assertIsInstance(self.player, Player)
        self.assertEqual(self.player.player_index, 0)
        self.assertEqual(self.player.number_of_players, 4)

    def test_on_new_turn(self):
        """Pick the card with the largest value in the player's hand."""

        card_values = [(2, 1), (3, 1), (1, 1), (4, 1)]
        hand = [self._make_card(v, bv) for v, bv in card_values]

        self.assertEqual(self.player.on_new_turn(hand, self.stacks),
                         self._make_card(4, 1))

    def test_on_cards_chosen(self):
        """Method does not do anything, and should return None."""

        self.assertIsNone(self.player.on_cards_chosen(self.discards))

    def test_choose_stack_to_take_stacks_all_equal(self):
        """If 2+ stacks have equal bull_value totals, pick the earliest."""
        stack_values = ([(85, 7), (86, 7), (87, 7), (88, 7)],
                        [(89, 7), (90, 7), (91, 7), (92, 7)],
                        [(93, 7), (94, 7), (95, 7), (96, 7)],
                        [(97, 7), (98, 7), (99, 7), (100, 7)], )
        stacks = self._make_stacks(stack_values)
        self.assertEqual(self.player.choose_stack_to_take(stacks), 0)

    def test_choose_stack_to_take_base(self):
        """Picks the stack with the lowest bull_value total."""

        self.assertEqual(self.player.choose_stack_to_take(self.stacks), 2)

    def test_choose_stack_to_take_min_stack(self):
        """If 2+ stacks have equal bull_value totals, pick the earliest."""
        stack_values = ([(61, 5)],
                        [(62, 2), (63, 2)],
                        [(64, 4)],
                        [(65, 7)], )
        stacks = self._make_stacks(stack_values)
        self.assertEqual(self.player.choose_stack_to_take(stacks), 1)

    def test_on_stacks_updated(self):
        """Method does not do anything, and should return None."""

        self.assertIsNone(self.player.on_stacks_updated(self.stacks))


if __name__ == '__main__':
    unittest.main()
