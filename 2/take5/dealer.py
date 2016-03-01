"""
This file contains the implementation of the Dealer component. The dealer is
responsible for managing the game, especially the rounds and turns.

The Dealer is given a list of Player objects and simulates a complete game.
A game ends when one of the players reaches a specified number of bull points at
the end of a round.
"""

import random

from definitions import create_deck
from player_state import PlayerState


TURNS_PER_ROUND = 10
MAX_BULL_POINTS = 66


class Dealer:

    def __init__(self, players):
        """ Creates a new Dealer
        :param players: list of players in the game
        """
        self.players = players
        self.player_states = []
        self.deck = None
        self.stacks = None
        self.turns = None
        self.max_bull_points = None

    def game(self, turns=TURNS_PER_ROUND, max_bull_points=MAX_BULL_POINTS):
        """ Simulates a complete game and returns the player id of the winner.
        :param turns: number of turns to be played / cards to be given out
        :param max_bull_points: maximum number of bull points each player can
                                have before a game ends
        :return: the player id of the winner
        """
        self.player_states = [PlayerState(player) for player in self.players]
        self.turns = turns
        self.max_bull_points = max_bull_points

        result = self.round(turns)

        while result is None:
            result = self.round(turns)

        return result

    def set_up_round(self, turns, player_states):
        """ Sets up the dealer for a new round
        :param turns: turns to be played in this round / cards to be handed out
        :param player_states: player states in the order the cards should be handed out
        :return: None
        """
        # hand out cards to each player
        for p in player_states:
            p.set_cards([self.deck.pop() for _ in range(turns)])

        self.stacks = tuple([self.deck.pop()] for _ in range(4))

    def check_for_winner(self):
        """ Checks if any player has more than the maximum number of bull points,
        and if so, returns the id of the player with the lowest number of bull points,
        otherwise returns none
        :return: player id of the winner or None
        """
        player_bull_points = [p.bull_points for p in self.player_states]

        if max(player_bull_points) >= self.max_bull_points:
            # the winner has the lowest number of points, in case of a tie the player
            # with the lowest player number wins
            return player_bull_points.index(min(player_bull_points))
        else:
            return None

    def round(self, turns):
        """ Simulate a round of the game
        :param turns: number of turns to play / cards to give to each player
        :return: the ID of the winning player, if there is one or None
        """
        self.deck = create_deck()
        random.shuffle(self.deck)

        self.set_up_round(turns, self.player_states)

        # perform the needed number of turns to discards all card from players
        for _ in range(turns):
            self.turn()

        return self.check_for_winner()

    def turn(self):
        """ Simulate a turn in a round of the game
        :return: None
        """
        chosen_cards = [p.choose_card(self.stacks) for p in self.player_states]
        # notify all players about the chosen cards
        for p in self.player_states:
            p.cards_chosen(chosen_cards)

        # cards are played from lowest to highest, sort on card value
        player_id_card_played = enumerate(chosen_cards)
        player_id_card_played_ordered = sorted(player_id_card_played, key=lambda x: x[1].value)

        for player_id, card in player_id_card_played_ordered:
            self.place_card_for_player(player_id, card)

    def pick_up_stack_and_replace_with_card(self, stack_index, new_card):
        """ Discard all cards in the given stack and return the combined value
        of their bull points.
        :param stack_index: index of the stack to replace
        :param new_card: new card to replace the stack with
        :return: combined number of bull points from the discarded cards
        """
        stack = self.stacks[stack_index]
        bull_points = 0
        while stack:
            bull_points += stack.pop().bullvalue
        # place the new card on the now empty stack
        stack.append(new_card)
        return bull_points

    def place_card_for_player(self, player_id, card):
        """ Places the given card on top of the appropriate stack, determines
        if a follow-up action has to take place and performs it.
        :param player_id: player id of the player who played the card
        :param card: card that was played
        :return: None
        """
        # stacks will never be empty
        topmost_card_values = [stack[-1].value for stack in self.stacks]
        player_state = self.player_states[player_id]

        # lowest card -> choose a stack and pick it up and replace with given card
        if card.value < min(topmost_card_values):
            stack_index = player_state.choose_stack(self.stacks)
            player_state.bull_points += self.pick_up_stack_and_replace_with_card(stack_index, card)

        # place on the stack with the largest card, lower than the given card
        else:
            card_value_to_place_on = max(x for x in topmost_card_values if x < card.value)
            stack_index = topmost_card_values.index(card_value_to_place_on)
            # if the stack had 5 cards -> pick up and replace with the given card
            stack = self.stacks[stack_index]
            if len(stack) == 5:
                player_state.bull_points += self.pick_up_stack_and_replace_with_card(stack_index, card)
            else:
                stack.append(card)

        for p in self.player_states:
            p.stacks_updated(self.stacks)

    def stats(self):
        """ Returns the statistics of the players at the current time, including
        the player id and the number of bull points they have, sorted
        by increasing number of bull points.
        :return: ordered list of player_id, bull points tuples
        """
        player_id_bull_points = [(i, p.bull_points) for i, p in enumerate(self.player_states)]
        player_id_bull_points.sort(key=lambda x: x[1])  # sort by bull points

        return [(player_id, bp) for player_id, bp in player_id_bull_points]
