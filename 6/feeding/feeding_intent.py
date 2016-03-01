"""
    Contains all feeding intents that can be returned by a Player as a
     response to a dealers's call to choose the next species to feed.
     Each intent implements a serialize method that generates a data
     representation for the intent according to the JSON data specification.

"""


class FeedingIntent:
    """ Represents a feeding intent, this class should never be used directly. """

    def serialize(self):
        """ Returns the appropriate data representation for the object
        :return: data representation
        """
        raise NotImplementedError()


class FeedNone(FeedingIntent):
    """ Represents the intention to not feed any species. """

    def serialize(self):
        return False


class FeedSpecies(FeedingIntent):
    """ Represents the intention to feed the given index of the species in the
     list of species of the current player. The Species at the index must not
     be fully fed."""
    def __init__(self, species_index):
        self.species_index = species_index

    def serialize(self):
        return self.species_index


class StoreFat(FeedSpecies):
    """ Represents the intention to store the given number of food tokens
     for the species at the given index. (The species must have the
     "fat tissue" trait) """
    def __init__(self, species_index, tokens):
        super().__init__(species_index)
        self.tokens = tokens

    def serialize(self):
        return [self.species_index, self.tokens]


class FeedVegetarian(FeedSpecies):
    """ Represents the intention to feed the vegetarian species at the given
     index in the Player's species list """
    pass


class FeedCarnivore(FeedSpecies):
    """ Represents the intention to feed the carnivore at the given index by
     attacking the species at defender_index of player at player_index. """
    def __init__(self, species_index, player_index, defender_index):
        super().__init__(species_index)
        self.player_index = player_index
        self.defender_index = defender_index

    def serialize(self):
        return [self.species_index, self.player_index, self.defender_index]