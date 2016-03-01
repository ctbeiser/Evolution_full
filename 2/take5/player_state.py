class PlayerState:
    """ Keeps track of the state of the given Player during a game,
    including the player's cards and the number of bull points.
    """

    def __init__(self, player):
        """ Adds point counting and card tracking to the given player
        :param player: Player object that controls this player
        """
        self.player = player
        self.cards = None
        self.bull_points = 0

    def set_cards(self, cards):
        """ Give the player the given list of cards
        :param cards: list of cards to give the player
        :return: None
        """
        self.cards = cards.copy()

    def choose_card(self, stacks):
        """ Ask the player to choose a card to discard
        :param stacks: the current stacks in game
        :return: the Card the player chose
        """
        card = self.player.on_new_turn(self.cards, stacks)
        self.cards.remove(card)
        return card

    def choose_stack(self, stacks):
        """ Ask the player to choose a stack to pick up
        :param stacks: the current stacks in game
        :return: the index of the stack to pick up
        """
        return self.player.choose_stack_to_take(stacks)

    def stacks_updated(self, stacks):
        """ Notify the player about the new state of stacks
        :param stacks: the current stacks in game
        :return: None
        """
        self.player.on_stacks_updated(stacks)

    def cards_chosen(self, cards):
        """ Notify the player about what cards each player has chosen
        :param cards: list of chosen cards, where the index corresponds to the player number
        :return: None
        """
        self.player.on_cards_chosen(cards)