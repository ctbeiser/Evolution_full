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
        """
        :param json: a python Array representing an Action4
        :return: a new Action4
        """
        assert(len(json) == NUMBER_OF_FIELDS)
        food_index = json[0]
        pops = [PopulationUpAction.deserialize(p) for p in json[1]]
        bodys = [BodyUpAction.deserialize(p) for p in json[2]]
        boards = [NewBoardAction.deserialize(p) for p in json[3]]
        replaces = [TraitReplaceAction.deserialize(p) for p in json[4]]
        return cls(food_index, pops, bodys, boards, replaces)

    def serialize(self):
        """
        :return: a python Array representing this Action4
        """
        return [self.food_index,
                [p.serialize() for p in self.grow_populations],
                [p.serialize() for p in self.grow_bodys],
                [p.serialize() for p in self.boards_with_traits],
                [p.serialize() for p in self.trait_replacements]]

    def verify(self, player):
        """ Ensure that there are no issues with the application of this Action4 to the given Player.
        :param player: a Player to verify against
        :return: True if this Action4 can be applied; else, False.
        """
        cards = self.card_indices()
        return (not(any(cards.count(x) > 1 for x in cards))) and (max(cards) <= len(player.cards))

    def enact(self, player):
        """ Carry out the actions on the given player and remove the TraitCard matching the food_index
        :param player: a Player to modify
        :return: The card placed in the Watering Hole
        """
        cards = self.card_indices()
        food_card = player.cards[self.food_index]
        for x in [self.grow_bodys, self.grow_populations, self.boards_with_traits, self.trait_replacements]:
            for act in x:
                act.enact(player)
        cards.sort()
        while cards:
            player.cards.remove(cards.pop())
        return food_card

    def card_indices(self):
        """
        :return: a List of Integers representing the cards used by this Action 4. Repeats indicate an improper Action4.
        """
        lists = [[[self.food_index]],
                 [p.cards() for p in self.grow_populations],
                 [p.cards() for p in self.grow_bodys],
                 [p.cards() for p in self.boards_with_traits],
                 [p.cards() for p in self.trait_replacements]]
        x = [cardlist for l in lists for cardlist in l]
        return [card for sublist in x for card in sublist]
