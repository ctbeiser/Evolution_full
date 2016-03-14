from .trait import Trait
from .player import Player
from .traitcard import TraitCard


class Dealer:
    def __init__(self, players, watering_hole, deck):
        """ Initialize a new Dealer
        :param players: A list of Player
        :param watering_hole: Integer
        :param deck: List of Trait_Card
        :return:
        """
        self.players = players
        self.watering_hole = watering_hole
        self.deck = deck or []

    def serialize(self):
        """ Produce a serialized representation of a Dealer according to the specification
        :return: An array of [LOP+, Natural, LOC]
        """
        return [self.players, self.watering_hole, self.deck]

    @classmethod
    def deserialize(cls, data):
        players = [Player.deserialize(p) for p in data[0]]
        wh = data[1]
        cards = [TraitCard.deserialize(i) for i in data[2]]
        return cls(players, wh, cards)

    def feed_one(self, players_feeding):
        """ Perform one round of feeding
        :param players_feeding: List of Players, with first to feed at the front
        """
        first_player = players_feeding[0]
        rest_players = [p for p in self.players if p is not first_player]

        intent = first_player.automatically_choose_species_to_feed(rest_players) or \
                 first_player.next_species_to_feed(rest_players, self.watering_hole)
        intent.enact(first_player, rest_players, self.feed_creature, self.fat_feed)

    def feed_creature(self, player, species_index, scavenge=False):
        """ Feed the creature from the watering hole if possible.
        It is safe to call this method on a full creature.
        :param player: Player on which the species is located
        :param species_index: Integer index of that species on the given Player
        :param scavenge: Boolean indicating whether creatures with scavenger should be fed.
        """
        species = player.species[species_index]

        if not (species.is_hungry() and self.watering_hole):
            return None

        feed_amount = min(1 + species.has_trait(Trait.FORAGING), self.watering_hole, species.population - species.food)
        species.food += feed_amount
        self.watering_hole -= feed_amount

        if species.has_trait(Trait.COOPERATION):
            right = player.get_neighbors(species)[1]
            if right:
                self.feed_creature(player, species_index+1)

        if scavenge:
            idx = self.players.index(player)
            for i in range(len(self.players)):
                player = self.players[(idx+i)%len(self.players)]
                for s in player.species:
                    if s.has_trait(Trait.SCAVENGER):
                        self.feed_creature(player, player.species.index(s))

    def fat_feed(self, player, species_index, tokens):
        """ Transfer fat food from the watering hole onto a player.
        It is assumed that the number of tokens will be legal.
        :param player: Player on which the species to feed is located
        :param species_index: Index of species on that player as an Integer
        :param tokens: Integer number of tokens to transfer from the watering hole
        """
        species = player.species[species_index]
        species.fat_food += tokens
        self.watering_hole -= tokens