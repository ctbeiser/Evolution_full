import unittest

from unittest.mock import MagicMock, call
from copy import deepcopy

from definitions import Card, create_deck
from dealer import Dealer, TURNS_PER_ROUND
from player_state import PlayerState
from dummy_player import DummyPlayer


class DealerTests(unittest.TestCase):

    def setUp(self):

        self.players = [
            DummyPlayer(0, 4),
            DummyPlayer(1, 4),
            DummyPlayer(2, 4),
            DummyPlayer(3, 4),
        ]
        self.deck = create_deck()

    @unittest.skip("")
    def test_turn(self):

        dealer = Dealer(self.players)
        dealer.stacks = (
            Card(1, 1),
            Card(2, 2),
            Card(3, 3),
            Card(4, 4)
        )

        for p in dealer.player_states:
            p.cards = [dealer.deck.pop() for _ in range(1)]

    def test_pick_up_stack_and_replace_with_card(self):

        card_1_1 = Card(1, 1)
        card_2_2 = Card(2, 2)
        card_10_3 = Card(10, 3)

        dealer = Dealer(self.players)
        dealer.stacks = (
            [card_1_1],
            [card_2_2, card_10_3],
            [Card(3, 3)],
            [Card(4, 4)]
        )

        original_stacks = deepcopy(dealer.stacks)

        new_card1 = Card(5, 6)
        new_card2 = Card(99, 1)

        # replace stack with one card
        sum_0 = dealer.pick_up_stack_and_replace_with_card(0, new_card1)
        self.assertEqual(sum_0, card_1_1.bullvalue)
        self.assertEqual(len(dealer.stacks), len(original_stacks))
        self.assertEqual(dealer.stacks[0], [new_card1])
        self.assertEqual(dealer.stacks[1], original_stacks[1])
        self.assertEqual(dealer.stacks[2], original_stacks[2])
        self.assertEqual(dealer.stacks[3], original_stacks[3])

        # replace stack with multiple cards
        sum_1 = dealer.pick_up_stack_and_replace_with_card(1, new_card2)
        self.assertEqual(sum_1, card_2_2.bullvalue + card_10_3.bullvalue)
        self.assertEqual(len(dealer.stacks), len(original_stacks))
        self.assertEqual(dealer.stacks[0], [new_card1])
        self.assertEqual(dealer.stacks[1], [new_card2])
        self.assertEqual(dealer.stacks[2], original_stacks[2])
        self.assertEqual(dealer.stacks[3], original_stacks[3])

    def test_place_card_for_player(self):

        dealer = Dealer(self.players)
        dealer.player_states = [PlayerState(player) for player in dealer.players]

        # card is the lowest one
        player_id = 0
        player_state = dealer.player_states[player_id]
        player_state.bull_points = 0

        new_card = Card(1, 1)
        card_7_7 = Card(7, 7)

        dealer.stacks = (
            [card_7_7],
            [Card(2, 2), Card(10, 3)],
            [Card(3, 3)],
            [Card(4, 4)]
        )

        # dummy player always choose first stack
        dealer.place_card_for_player(player_id, new_card)
        self.assertEqual(player_state.bull_points, card_7_7.bullvalue)

        # card is higher than 1 other card
        player_id = 0
        player_state = dealer.player_states[player_id]
        player_state.bull_points = 0

        new_card = Card(8, 1)
        card_7_7 = Card(7, 7)
        card_3_4 = Card(3, 4)

        dealer.stacks = (
            [Card(2, 2), Card(10, 3)],
            [card_3_4, card_7_7],
            [Card(30, 3)],
            [Card(40, 4)]
        )

        # no stack is picked up in this case
        dealer.place_card_for_player(player_id, new_card)
        self.assertEqual(player_state.bull_points, 0)
        self.assertEqual(dealer.stacks[1], [card_3_4, card_7_7, new_card])

        # card is higher than all other cards
        player_id = 0
        player_state = dealer.player_states[player_id]
        player_state.bull_points = 0

        new_card = Card(80, 1)
        card_7_7 = Card(7, 7)
        card_3_4 = Card(3, 4)

        dealer.stacks = (
            [Card(2, 2), Card(10, 3)],
            [card_3_4, card_7_7],
            [Card(30, 3)],
            [Card(40, 4)]
        )

        # no stack is picked up in this case
        dealer.place_card_for_player(player_id, new_card)
        self.assertEqual(player_state.bull_points, 0)
        self.assertEqual(dealer.stacks[3], [Card(40, 4), new_card])

        # stack had 5 cards
        player_id = 0
        player_state = dealer.player_states[player_id]
        player_state.bull_points = 0

        new_card = Card(11, 1)
        card_7_7 = Card(7, 7)
        card_3_4 = Card(3, 4)
        card_8_2 = Card(8, 2)
        card_9_3 = Card(9, 3)
        card_10_3 = Card(10, 3)

        dealer.stacks = (
            [Card(2, 2), Card(12, 3)],
            [Card(30, 3)],
            [card_3_4, card_7_7, card_8_2, card_9_3, card_10_3],
            [Card(40, 4)]
        )

        # no stack is picked up in this case
        dealer.place_card_for_player(player_id, new_card)
        self.assertEqual(player_state.bull_points,
                         card_3_4.bullvalue + card_7_7.bullvalue +
                         card_8_2.bullvalue + card_9_3.bullvalue +
                         card_10_3.bullvalue)
        self.assertEqual(dealer.stacks[2], [new_card])

    def test_turn(self):

        dealer = Dealer(self.players)
        dealer.player_states = [PlayerState(p) for p in dealer.players]
        dealer.stacks = (
            [Card(1, 1)],
            [Card(2, 2)],
            [Card(3, 3)],
            [Card(4, 4)]
        )

        chosen_cards = []
        for i, p in enumerate(dealer.player_states):
            chosen_card = Card(i, 1)
            chosen_cards.append(chosen_card)
            p.choose_card = MagicMock(return_value=chosen_card)
            p.cards_chosen = MagicMock(return_value=chosen_cards)

        dealer.place_card_for_player = MagicMock()
        dealer.turn()

        for p in dealer.player_states:
            p.choose_card.assert_called_once_with(dealer.stacks)
            p.cards_chosen.assert_called_once_with(chosen_cards)

        calls = [call(i, card) for i, card in enumerate(chosen_cards)]
        dealer.place_card_for_player.assert_has_calls(calls)

    def test_turn_reverse_order(self):

        dealer = Dealer(self.players)
        dealer.player_states = [PlayerState(p) for p in dealer.players]
        dealer.stacks = (
            [Card(1, 1)],
            [Card(2, 2)],
            [Card(3, 3)],
            [Card(4, 4)]
        )

        chosen_cards = []
        for i, p in enumerate(dealer.player_states):
            chosen_card = Card(10 - i, 1)
            chosen_cards.append(chosen_card)
            p.choose_card = MagicMock(return_value=chosen_card)
            p.cards_chosen = MagicMock(return_value=chosen_cards)

        dealer.place_card_for_player = MagicMock()
        dealer.turn()

        for p in dealer.player_states:
            p.choose_card.assert_called_once_with(dealer.stacks)
            p.cards_chosen.assert_called_once_with(chosen_cards)

        calls = [call(i, card) for i, card in enumerate(chosen_cards)]
        calls.reverse()
        dealer.place_card_for_player.assert_has_calls(calls)

    def test_set_up_round(self):

        for turns in range(10):

            unshuffled_deck = create_deck()
            dealer = Dealer(self.players)
            dealer.player_states = [PlayerState(p) for p in dealer.players]
            dealer.deck = unshuffled_deck

            # deck in order the cards are handed out
            deck_in_order = unshuffled_deck.copy()
            deck_in_order.reverse()

            for p in dealer.player_states:
                p.set_cards = MagicMock()

            dealer.set_up_round(turns, dealer.player_states)

            for i, p in enumerate(dealer.player_states):
                cards_start = i * turns
                cards_end = (i + 1) * turns
                p.set_cards.assert_called_once_with(deck_in_order[cards_start:cards_end])

            num_players = len(dealer.player_states)
            self.assertEqual(dealer.stacks, (
                [deck_in_order[num_players * turns]],
                [deck_in_order[num_players * turns + 1]],
                [deck_in_order[num_players * turns + 2]],
                [deck_in_order[num_players * turns + 3]],
            ))

    def test_check_for_winner(self):

        players = [
            DummyPlayer(0, 4),
            DummyPlayer(1, 4),
            DummyPlayer(2, 4),
            DummyPlayer(3, 4),
        ]

        dealer = Dealer(players)
        dealer.player_states = [PlayerState(p) for p in dealer.players]
        dealer.max_bull_points = 66

        # no winner
        dealer.player_states[0].bull_points = 30
        dealer.player_states[1].bull_points = 20
        dealer.player_states[2].bull_points = 10
        dealer.player_states[3].bull_points = 40

        self.assertIsNone(dealer.check_for_winner())

        # player #2 is the winner
        dealer.player_states[0].bull_points = 30
        dealer.player_states[1].bull_points = 20
        dealer.player_states[2].bull_points = 10
        dealer.player_states[3].bull_points = 66

        self.assertEqual(dealer.check_for_winner(), 2)

        # player #1, #2 are tied, but 1 is first
        dealer.player_states[0].bull_points = 30
        dealer.player_states[1].bull_points = 20
        dealer.player_states[2].bull_points = 20
        dealer.player_states[3].bull_points = 70

        self.assertEqual(dealer.check_for_winner(), 1)

    def test_round(self):

        dealer = Dealer(self.players)
        dealer.max_bull_points = 100
        dealer.player_states = [PlayerState(p) for p in dealer.players]

        turns = 5

        dealer.set_up_round = MagicMock()
        dealer.turn = MagicMock()
        dealer.check_for_winner = MagicMock()

        dealer.round(turns)

        dealer.set_up_round.assert_called_once_with(turns, dealer.player_states)
        dealer.check_for_winner.assert_called_once_with()
        self.assertEqual(len(dealer.turn.mock_calls), turns)

    def test_print_stats(self):

        players = [
            DummyPlayer(0, 4),
            DummyPlayer(1, 4),
            DummyPlayer(2, 4),
            DummyPlayer(3, 4),
        ]

        dealer = Dealer(players)
        dealer.player_states = [PlayerState(p) for p in dealer.players]

        dealer.player_states[0].bull_points = 10
        dealer.player_states[1].bull_points = 20
        dealer.player_states[2].bull_points = 30
        dealer.player_states[3].bull_points = 40

        self.assertEqual(dealer.stats(), [
            (0, dealer.player_states[0].bull_points),
            (1, dealer.player_states[1].bull_points),
            (2, dealer.player_states[2].bull_points),
            (3, dealer.player_states[3].bull_points),

        ])

        dealer.player_states[0].bull_points = 50
        dealer.player_states[1].bull_points = 30
        dealer.player_states[2].bull_points = 20
        dealer.player_states[3].bull_points = 10

        self.assertEqual(dealer.stats(), [
            (3, dealer.player_states[3].bull_points),
            (2, dealer.player_states[2].bull_points),
            (1, dealer.player_states[1].bull_points),
            (0, dealer.player_states[0].bull_points),

        ])

    def test_game(self):

        dealer = Dealer(self.players)
        dealer.round = MagicMock()

        # player number 2 won
        dealer.round.return_value = 2
        self.assertEqual(dealer.game(), 2)
        dealer.round.assert_called_once_with(TURNS_PER_ROUND)

        dealer.round.reset_mock()
        # player number 3 won, but in the third round
        dealer.round.side_effect = [None, None, 3]
        self.assertEqual(dealer.game(), 3)
        dealer.round.assert_has_calls([call(TURNS_PER_ROUND)] * 3)




