from .trait import Trait

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
        elif len(data) == 2:
            return StoreFat(*data)
        elif len(data) == 3:
            return FeedCarnivore(*data)
        else:
            assert(False)

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
        self.species_index = species_index

    def serialize(self):
        return self.species_index

    def deserialize(self, data):
        self.init(*data)


class StoreFat(FeedSpecies):
    """ Represents the intention to store the given number of food tokens
     for the species at the given index. (The species must have the
     "fat tissue" trait) """
    def __init__(self, species_index, tokens):
        super().__init__(species_index)
        self.tokens = tokens

    def serialize(self):
        return [self.species_index, self.tokens]

    def enact(self, player, others, dealer):
        dealer.fat_feed(player, self.species_index, self.tokens)


class FeedVegetarian(FeedSpecies):
    """ Represents the intention to feed the vegetarian species at the given
     index in the Player's species list """
    def enact(self, player, others, dealer):
        print("Feeding")
        dealer.feed_creature(player, self.species_index)


class FeedCarnivore(FeedSpecies):
    """ Represents the intention to feed the carnivore at the given index by
     attacking the species at defender_index of player at player_index. """
    def __init__(self, species_index, defending_player_index, defender_index):
        super().__init__(species_index)
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