from .species import Species


class Action:
    def cards(self):
        """
        :return: A List of Positive Integer indexes of the cards used by this Action
        """
        return []

    def enact(self, player):
        """ Carry out the purpose of the Action on the given player.
        :param player: A Player, who will be mutated.
        """
        pass


class UpAction(Action):
    def __init__(self, board, card):
        """
        :param board: Integer representing the index of the Board to grow population of
        :param card: Integer representing the index of the Card to exchange to grow
        :return: A new *UpAction
        """
        self.board = board
        self.card = card

    def cards(self):
        return [self.card]

    @classmethod
    def deserialize(cls, json):
        """ Create an *UpAction from a JSON input
        :param json: A JSON representation of an *UpAction
        :return: A new *UpAction
        """
        board = json[1]
        card = json[2]
        return cls(board, card)


class PopulationUpAction(UpAction):
    """
    Represents an 'increase population' Action
    """
    def enact(self, player):
        """
        :param player: The player whose population should be increased.
        """
        creature = player.species[self.board]
        creature.population += 1

    def serialize(self):
        """
        :return: A python Array representing this action as JSON
        """
        return ["population", self.board, self.card]


class BodyUpAction(UpAction):
    """
    Represents an 'increase body size' action
    """
    def enact(self, player):
        creature = player.species[self.board]
        creature.body += 1

    def serialize(self):
        """
        :return: A python Array representing this action as JSON
        """
        return ["body", self.board, self.card]


class NewBoardAction(Action):
    """
    Represents an "insert new Board" action
    """
    def __init__(self, card_for_board, other_cards):
        """
        :param card_for_board: An Integer, representing which card should be used to  buy the new Board
        :param other_cards: A list of Integers, length 0-3, representing the TraitCards that should be placed on it
        """
        self.card_for_board = card_for_board
        self.other_cards = other_cards or []

    @classmethod
    def deserialize(cls, json):
        """
        :param json: A python Array representing this action as JSON
        :return: a new NewBoardAction
        """
        b = json.pop(0)
        o = json
        return cls(b, o)

    def cards(self):
        return self.serialize()

    def serialize(self):
        """
        :return: A python Array representing this action as JSON
        """
        x = [card for card in self.other_cards]
        x.insert(0, self.card_for_board)
        return x

    def enact(self, player):
        """ Adds a new Board to the given Player.
        :param player: A Player to mutate
        :return:
        """
        hand = player.cards
        traits = [hand[c].trait for c in self.other_cards]
        player.species.append(Species(traits=traits))


class TraitReplaceAction(Action):
    """
    Represents an action that replaces Traits with new ones.
    """
    def __init__(self, board, idx_replace, with_card):
        """
        :param board: The Integer index of the board to replace on the Player
        :param idx_replace: the Integer index on the Species of which Trait to replace
        :param with_card: the Integer index of TraitCard with which to replace the trait with.
        """
        self.board = board
        self.idx_replace = idx_replace
        self.with_card = with_card

    def cards(self):
        return [self.with_card]

    @classmethod
    def deserialize(cls, json):
        """
        :param json: A python Array representing this action as JSON
        :return: a new TraitReplaceAction
        """
        return cls(*json)

    def serialize(self):
        """
        :return: a Python array representing this action as JSON
        """
        return [self.board, self.idx_replace, self.with_card]

    def enact(self, player):
        """ Replace the trait on the given player.
        :param player: a Player
        """
        card = player.cards[self.with_card].trait
        player.species[self.board].replace_trait_at_index(self.idx_replace, card)
