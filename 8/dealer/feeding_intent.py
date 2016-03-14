from trait import Trait

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

    def enact(self, player, others, feed, fat_feed):
        """ Modifies players to carry out this feeding
        :param player: Player that is feeding
        :param others: List of the other Players
        :param feed: A function to feed a creature, documented as feed_creature in Dealer.py
        :param fat_feed: A function to feed a creature fat tokens, documented as fat_feed in Dealer.py
        """
        pass


class CannotFeed(FeedingIntent):
    """ Represents the inability to feed any species. """

    def serialize(self):
        raise ValueError("Cannot feed cannot be serialized.")


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

    def enact(self, player, others, feed, fat_feed):
        fat_feed(player, self.species_index, self.tokens)


class FeedVegetarian(FeedSpecies):
    """ Represents the intention to feed the vegetarian species at the given
     index in the Player's species list """
    def enact(self, player, others, feed, fat_feed):
        feed(player, self.species_index)


class FeedCarnivore(FeedSpecies):
    """ Represents the intention to feed the carnivore at the given index by
     attacking the species at defender_index of player at player_index. """
    def __init__(self, species_index, player_index, defender_index):
        super().__init__(species_index)
        self.player_index = player_index
        self.defender_index = defender_index

    def serialize(self):
        return [self.species_index, self.player_index, self.defender_index]

    def enact(self, player, others, feed, fat_feed):
        defender = others[self.player_index].species[self.defender_index]
        attacker = player.species[self.species_index]
        has_horns = defender.has_trait(Trait.HORNS)

        defender.population -= 1
        attacker.population -= has_horns

        if defender.population == 0:
            others[self.player_index].species.pop(self.defender_index)

        if attacker.population == 0:
            player.species.pop(self.species_index)

        else:
            feed(player, self.species_index, scavenge=True)
