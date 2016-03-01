"""
Implements a Player according to the player interface specification from project 1.
The strategy for this player is the following:
    1. when asked to discard a card the player chooses the one with the largest value
    2. when asked to pick a stack to take the player chooses the one with the lowest
        amount of bull points
"""


class Player:

    def __init__(self, player_index, number_of_players):
        """ Initializes a new player
        @param player_index: this player's position around the table, indexed from 0
        @param number_of_players: the number of players at the table.
        """
        pass

    def on_new_turn(self, hand, stacks):
        """ Called on the start of a turn. Used to choose the card to play that  turn
        @param hand: a list of Card that represents the player's hand
        @param stacks: a Stacks representing the state of the board
        @return: a Card to be discarded
        """
        return max(hand, key=lambda card: card.value)

    def on_cards_chosen(self, discards):
        """ Called when all players have passed in their cards for the turn
        @param discards: a list of Card, where index corresponds to the player number
        """
        pass

    def choose_stack_to_take(self, stacks):
        """ Called when a player is required to choose a stack to take, per the rules
        @param stacks: a Stacks representing the stacks available to take
        @return: the index of the chosen stack
        """
        stack_values = [sum(card.bullvalue for card in stack) for stack in stacks]
        return stack_values.index(min(stack_values))

    def on_stacks_updated(self, stacks):
        """ Called whenever the stacks on the board are updated
        @param stacks: a Stacks representing the state of the board
        """
        pass
