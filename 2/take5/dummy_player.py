"""

This file implements the Player interface for testing. This dummy player
always returns the first card from the hand and always chooses to pick
up the first stack, when asked.

A Card is a namedtuple of (value, bullvalue), where value is a Value, and
    bullvalue is a BullValue
A Value is an Integer in the range [1, 104]
A BullValue is an Integer in the range [1, 7]
A Stacks is a 4-tuple of list of Card, with the bottom of the stack first

"""


class DummyPlayer:

    def __init__(self, player_index, number_of_players):
        """ Initializes a new player
        @param player_index: this player's position around the table, indexed from 0
        @param number_of_players: the number of players at the table.
        """
        self.index = player_index
        self.number_of_players = number_of_players

    def on_new_turn(self, hand, stacks):
        """ Called on the start of a turn. Used to choose the card to play that  turn
        @param hand: a list of Card that represents the player's hand
        @param stacks: a Stacks representing the state of the board
        @return: a Card to be discarded
        """
        return hand[0]

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
        return 0

    def on_stacks_updated(self, stacks):
        """ Called whenever the stacks on the board are updated
        @param stacks: a Stacks representing the state of the board
        """
        pass