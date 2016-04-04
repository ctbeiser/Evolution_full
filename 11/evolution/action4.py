from .action import *

NUMBER_OF_FIELDS = 5


class Action4:
    def __init__(self, food_index, grow_populations, grow_bodys, boards_with_traits, trait_replacements):
        """
        Creates a new Actions, listing changes to be made in step 4 of Evolution, and verifies them.
        :param food_index: Natural indicating which card is turned into food.
        :param grow_populations: A list of PopulationUpActions to carry out.
        :param grow_bodys: A list of BodyUpActions to carry out
        :param boards_with_traits: A list of NewBoardActions to carry out
        :param trait_replacements: A list of TraitReplaceActions to carry out
        :return: a new Action4
        """
        self.food_index = food_index
        self.grow_populations = grow_populations
        self.grow_bodys = grow_bodys
        self.boards_with_traits = boards_with_traits
        self.trait_replacements = trait_replacements

    @classmethod
    def deserialize(cls, json):
        assert(len(json) == NUMBER_OF_FIELDS)
        food_index = json[0]
        pops = [PopulationUpAction.deserialize(p) for p in json[1]]
        bodys = [BodyUpAction.deserialize(p) for p in json[2]]
        boards = [NewBoardAction.deserialize(p) for p in json[3]]
        replaces = [TraitReplaceAction.deserialize(p) for p in json[4]]
        return cls(food_index, pops, bodys, boards, replaces)

    def serialize(self):
        return [self.food_index,
                [p.serialize() for p in self.grow_populations],
                [p.serialize() for p in self.grow_bodys],
                [p.serialize() for p in self.boards_with_traits],
                [p.serialize() for p in self.trait_replacements]]

    def verify(self, player):
        cards = self.card_indices()
        conditions = [len(cards) == len(set(cards)),
                      max(cards) <= len(player.cards)]
        return all(conditions)

    def card_indices(self):
        lists = [[self.food_index],
                 [p.cards() for p in self.grow_populations],
                 [p.cards() for p in self.grow_bodys],
                 [p.cards() for p in self.boards_with_traits],
                 [p.cards() for p in self.trait_replacements]]
        return [card for l in lists for card in l]
