

class Player(object):
    """A player component in the 6Nimmt! game.

    This player pursues a basic strategy:
        -- When asked to discard, it picks the highest card in its hand.
        -- When asked to pick a stack, it picks the stack with the lowest bull
           number total.
    """
    MAX_STACK_BULL_VALUE = 28

    def __init__(self, player_index, number_of_players):
        """Initializes a new player

        @param player_index: player's position around the table, indexed from 0
        @param number_of_players: the number of players at the table.
        """
        self.player_index = player_index
        self.number_of_players = number_of_players

    def on_new_turn(self, hand, stacks):
        """Called on the start of a turn. Used to choose the card to play

        @param hand: a list of Card that represents the player's hand
        @param stacks: a Stacks representing the state of the board
        @returns a Card to be discarded

        Preconditions:
            -- Each card in the hand must have a different value.

        This player always picks the card with the highest Value.
        """
        return max(hand, key=lambda c: c.value)

    def on_cards_chosen(self, discards):
        """Called when all players have passed in their cards for the turn

        @param discards: a list of Card, where index is the player number
        """
        # Player does not need to know discards to play its strategy
        pass

    def choose_stack_to_take(self, stacks):
        """Called when a player is required to choose a stack to take

        @param stacks: a Stacks representing the stacks available to take
        @return: the index of the chosen stack

        Preconditions:
            -- Each list in stacks must be non-empty

        This player always takes the stack with the smallest bull_value total.
        If two stacks have the same total, we return the smaller index.
        """
        min_bull_value = self.MAX_STACK_BULL_VALUE
        min_stack_index = 0
        for i, stack in enumerate(stacks):
            stack_bull_value = sum(card.bullvalue for card in stack)

            if stack_bull_value < min_bull_value:
                min_bull_value = stack_bull_value
                min_stack_index = i
        return min_stack_index

    def on_stacks_updated(self, stacks):
        """Called whenever the stacks on the board are updated

        @param stacks: a Stacks representing the state of the board
        """
        # Player does not need to track stacks since they're provided in
        # on_new_turn() and choose_stack_to_take()
        pass
