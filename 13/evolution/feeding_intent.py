from .trait import Trait
from .validate import *

"""
    Contains all feeding intents that can be returned by a Player as a
     response to a dealers's call to choose the next species to feed.
     Each intent implements a serialize method that generates a data
     representation for the intent according to the JSON data specification.
"""


class FeedingIntent:
    """ Represents a feeding intent— this class should never be used directly. """

    def serialize(self):
        """ Returns the appropriate data representation for the object
        :return: data representation
        """
        raise NotImplementedError()

    @staticmethod
    def deserialize(data):
        """ Given a feeding intent as JSON, return the proper FeedingIntent
        :param data: a JSON representation of a FeedingIntent
        :return: a new FeedingIntent
        """
        if data is False:
            return FeedNone()
        elif isinstance(data, int):
            return FeedVegetarian(data)
        elif is_list(data):
            if len(data) == 2:
                return StoreFat(*data)
            if len(data) == 3:
                return FeedCarnivore(*data)
        raise ValueError("This is not a valid Feeding Intent")

    def enact(self, player, others, dealer):
        """ Modifies players to carry out this feeding
        :param player: Player that is feeding
        :param others: List of the other Players
        :param dealer: the Dealer with which to carry out the necessary changes
        """
        pass

    def should_end_feeding(self):
        """
        :return: a Boolean indicating whether feeding should be ended for this Player
        """
        return False

    def is_valid(self, player, others, wh):
        """ Check whether this feeding can be carried out given the state of the game
        :param player: Player that is feeding
        :param others: List of the other Players
        :param wh: the watering hole on which to check for validity
        :return: a Boolean indicating whether this feeding is invalid for the given dealer
        """
        return True

class CannotFeed(FeedingIntent):
    """ Represents the inability to feed any species. """

    def serialize(self):
        raise ValueError("Cannot feed cannot be serialized.")

    def should_end_feeding(self):
        return True

class FeedNone(FeedingIntent):
    """ Represents the intention to not feed any species. """

    def serialize(self):
        return False

    def should_end_feeding(self):
        return True


class FeedSpecies(FeedingIntent):
    """ Represents the intention to feed the given index of the species in the
     list of species of the current player. The Species at the index must not
     be fully fed."""
    def __init__(self, species_index):
        if not is_natural(species_index):
            raise ValueError("The index of the player is not legal.")
        self.species_index = species_index

    def serialize(self):
        return self.species_index

    def is_valid(self, player, others, wh):
        return self.species_index in range(len(player.species))


class StoreFat(FeedSpecies):
    """ Represents the intention to store the given number of food tokens
     for the species at the given index. (The species must have the
     "fat tissue" trait) """
    def __init__(self, species_index, tokens):
        super().__init__(species_index)
        if not is_natural_plus(tokens):
            raise ValueError("There must be at least one fat token.")
        self.tokens = tokens

    def serialize(self):
        return [self.species_index, self.tokens]

    def enact(self, player, others, dealer):
        dealer.fat_feed(player, self.species_index, self.tokens)

    def is_valid(self, player, others, wh):
        if not super(StoreFat, self).is_valid(player, others, wh):
            return False
        species = player.species[self.species_index]
        return all([wh >= self.tokens,
                   species.has_trait(Trait.FAT_TISSUE),
                   species.fat_food + self.tokens <= species.body])


class FeedVegetarian(FeedSpecies):
    """ Represents the intention to feed the vegetarian species at the given
     index in the Player's species list """
    def enact(self, player, others, dealer):
        dealer.feed_creature(player, self.species_index)


class FeedCarnivore(FeedSpecies):
    """ Represents the intention to feed the carnivore at the given index by
     attacking the species at defender_index of player at player_index. """
    def __init__(self, species_index, defending_player_index, defender_index):
        super().__init__(species_index)
        if not is_natural(defending_player_index) and is_natural(defender_index):
            raise ValueError("This FeedCarnivore has been passed invalid data")
        self.defending_player_index = defending_player_index
        self.defender_index = defender_index

    def serialize(self):
        return [self.species_index, self.defending_player_index, self.defender_index]

    def enact(self, player, others, dealer):
        defender = others[self.defending_player_index].species[self.defender_index]
        attacker = player.species[self.species_index]
        has_horns = defender.has_trait(Trait.HORNS)

        defender.population -= 1
        attacker.population -= has_horns
        if defender.population == 0:
            dealer.kill_creature(others[self.defending_player_index], self.defender_index)
        if attacker.population == 0:
            dealer.kill_creature(player, self.species_index)

        else:
            dealer.feed_creature(player, self.species_index, scavenge=True)

    def is_valid(self, player, others, wh):
        return super(FeedCarnivore, self).is_valid(player, others, wh) \
            and self.defending_player_index in range(len(others)) \
            and self.defender_index in range(len(others[self.defending_player_index].species))
