""" Represents a Player for the Evolution game
"""

from .trait import Trait

from .species import Species
from .feeding_intent import FeedNone, StoreFat, FeedVegetarian, FeedCarnivore, CannotFeed

DEFAULT_BAG_VALUE = 0


class Player:

    def __init__(self, player_id, species=None, bag=DEFAULT_BAG_VALUE):
        """ Initialize a new Player
        :param player_id: id of the player as a Natural number greater than 0
        :param species: a list of Species or None
        :param bag: number of food tokens in the bag
        """
        self.player_id = player_id
        self.species = species or []
        self.bag = bag

    def serialize(self):
        """ Returns a serialized version of the Player
        :return: serialized version of the Player
        """
        return [
            ["id", self.player_id],
            ["species", [species.serialize() for species in self.species]],
            ["bag", self.bag],
        ]

    @classmethod
    def deserialize(cls, data):
        """ Returns a serialized version of the Player
        :return: serialized version of the Player
        """
        parameters = {parameter: value for parameter, value in data}

        assert 'id' in parameters
        assert 'species' in parameters
        assert 'bag' in parameters

        species = [Species.deserialize(species) for species in parameters['species']]

        return cls(
            player_id=parameters['id'],
            species=species,
            bag=parameters['bag'],
        )

    @staticmethod
    def _find_max_values(values, key):
        """ Returns a list of maximum values given a key.
        :param values: list of values
        :param key: value -> sortable value
        :return: list all elements tied for first place
        """
        max_key = max(key(v) for v in values)
        return [v for v in values if key(v) == max_key]

    @staticmethod
    def species_ordering_key(species):
        """ Generates a sorting key for the given species.

          Species are ordered in a lexicographic manner, starting with
           the (plain) population attribute, followed by the food that
           the species has been fed so far, and finally the (plain) body size.

        :param species: species to generate a sorting key for
        :return: sorting key for the given species
        """
        return -species.population, -species.food, -species.body

    def order_species(self, species_list):
        """ Orders the given list of species that is a subset of the player's
         species, based on the following ordering:

         If there are any ties, then species are placed in the order of the
         species boards.

        :param species_list: subset of the player's species as a list
        :return: order list of species
        """
        def leftmost_ordering(species):
            return self.species.index(species)

        def ordering(species):
            return self.species_ordering_key(species), leftmost_ordering(species)

        return sorted(species_list, key=ordering)

    def _get_neighbors(self, species):
        """ Returns the left and right neighbor of the given species.
        :param species: species to find the neighbors of
        :return: a tuple of (left, right) neighbor, where either can be None
        """
        species_length = len(self.species)

        species_position = self.species.index(species)
        left = self.species[species_position - 1] if species_position > 0 else None
        right = self.species[species_position + 1] if species_position < (species_length - 1) else None

        return left, right

    def get_attackable_species(self, attacker):
        """ Returns all species of this player that are attackable by the
         given species.
        :param attacker: the attacking species
        :return: list of species attackable by the attacker
        """
        def is_attackable(species):
            left, right = self._get_neighbors(species)
            return species.is_attackable(attacker, left=left, right=right)

        return [species for species in self.species if is_attackable(species)]

    def next_species_to_feed(self, players, watering_hole):
        """ Determines the next species to feed, given the other players
        in the game.
        :param players: list of Player
        :param watering_hole: number of food tokens in the watering hole
        :return: FeedingIntention
        """
        return (self.feed_fat_tissue(watering_hole) or
                self.feed_vegetarian() or
                self.feed_carnivore(players) or
                self.feed_on_own() or
                CannotFeed())

    def feed_fat_tissue(self, watering_hole):
        """ Returns an intent to store the specified number of food tokens
         on the largest species with the "fat tissue" trait. If there are
         no suitable species returns None
        :param watering_hole: number of food tokens in the watering hole
        """
        species_with_fat_tissue = [species for species in self.species
                                   if species.has_trait(Trait.FAT_TISSUE) and
                                   species.fat_food < species.body]
        # greatest need for fat food: the body size of the species
        if len(species_with_fat_tissue) > 0:
            species_with_greatest_need = self._find_max_values(species_with_fat_tissue,
                                                               lambda species: species.body)

            eater = self.order_species(species_with_greatest_need)[0]
            food_to_request = min(eater.body - eater.fat_food, watering_hole)
            return StoreFat(self.species.index(eater), food_to_request)

    def feed_vegetarian(self):
        """ Returns an intent to feed the largest hungry vegetarian species
         belonging to this player or None if there are no hungry vegetarians.
        :return: intent to feed the largest hungry vegetarian or None
        """
        vegetarians = [species for species in self.species
                       if not species.has_trait(Trait.CARNIVORE) and species.is_hungry()]

        if len(vegetarians) > 0:
            eater = self.order_species(vegetarians)[0]
            return FeedVegetarian(self.species.index(eater))

    def feed_carnivore(self, players):
        """ Finds the largest carnivore that can attack any of the given
         player's species and chooses the largest species to attack. Returns
         an intent to attack with the largest carnivore the largest species
         of a given player.

         If no carnivore can attack any of the other player's species
         returns None.

        :param players: other players in the game
        :return: intent to attack or None
        """
        carnivores = [species for species in self.species
                      if species.has_trait(Trait.CARNIVORE) and species.is_hungry()]

        if len(carnivores) > 0:
            eater_candidates = self.order_species(carnivores)

            for candidate in eater_candidates:
                eater = candidate
                attackable_species = [player.get_attackable_species(candidate) for player in players]
                # if there are no attackable species move on to the next candidate
                if not any(attackable_species):
                    continue

                largest_attackable = []

                for player, player_attackable_species in zip(players, attackable_species):
                    if not player_attackable_species:
                        continue

                    player_largest_attackable = player.order_species(player_attackable_species)[0]
                    largest_attackable.append((player_largest_attackable, player))

                def defender_player_key(species_player):
                    """ Sorts defender_player list based on largest species and then player id"""
                    species, player = species_player
                    return self.species_ordering_key(species)

                defender, player = sorted(largest_attackable, key=defender_player_key)[0]

                return FeedCarnivore(
                    self.species.index(eater),
                    players.index(player),
                    player.species.index(defender)
                )

    def feed_on_own(self):
        """ Checks if the player can feed on one of their species. If so
         an intent not to feed will be returned as the Player doesn't want
         to attack their own species.

        :return: FeedingIntent or None
        """
        can_attack_own = self.feed_carnivore([self])
        return FeedNone() if can_attack_own else None
