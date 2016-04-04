from .player import Player
from .species import Species


class Action:
    def cards(self):
        return []

    def enact(self, player):
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
        """
        :return: All cards that this method will use.
        """
        return [self.card]

    @classmethod
    def deserialize(cls, json):
        board = json[1]
        card = json[2]
        return cls(board, card)


class PopulationUpAction(UpAction):
    def enact(self, player):
        creature = player.species[self.board]
        creature.population += 1

    def serialize(self):
        return ["population", self.board, self.card]


class BodyUpAction(UpAction):
    def enact(self, player):
        creature = player.species[self.board]
        creature.body += 1

    def serialize(self):
        return ["body", self.board, self.card]


class NewBoardAction(Action):
    def __init__(self, card_for_board, other_cards):
        self.card_for_board = card_for_board
        self.other_cards = other_cards or []

    @classmethod
    def deserialize(cls, json):
        b = json.pop(0)
        o = json
        return cls(b, o)

    def cards(self):
        return self.serialize()

    def serialize(self):
        x = [card for card in self.other_cards]
        x.insert(0, self.card_for_board)
        return x

    def enact(self, player):
        hand = player.cards
        traits = [hand[c].trait for c in self.other_cards]
        player.species.append(Species(traits=traits))


class TraitReplaceAction(Action):
    def __init__(self, board, idx_replace, with_card):
        self.board = board
        self.idx_replace = idx_replace
        self.with_card = with_card

    def cards(self):
        return [self.with_card]

    @classmethod
    def deserialize(cls, json):
        return cls(*json)

    def serialize(self):
        return [self.board, self.idx_replace, self.with_card]

    def enact(self, player):
        card = player.cards[self.with_card].trait
        player.species[self.board].replace_trait_at_index(self.idx_replace, card)
