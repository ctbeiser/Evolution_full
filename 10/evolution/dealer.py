from .trait import Trait
from .player import Player
from .traitcard import TraitCard

DEAD_CREATURE_REPLACEMENT_CARDS = 2


class Dealer:
    """
    Represents a Dealer in the game of Evolution.
    """
    def __init__(self, players, watering_hole, deck=None):
        """ Initialize a new Dealer
        :param players: A list of Player
        :param watering_hole: Integer
        :param deck: List of Trait_Card
        :return:
        """
        self.players = players
        self.watering_hole = watering_hole
        self.deck = deck or []

    def make_tree(self, tree, parent):
        """ Modify the ttk tree provided to add a representation of this data structure
        :param tree: a ttk Treeview widget object
        :param parent: the ttk reference to a row in the ttk Treeview under which this content should be added.
        """
        tree.insert(parent, 'end', text=("Watering Hole: " + str(self.watering_hole)))
        players = tree.insert(parent, 'end', text="Players")
        for p in self.players:
            p.make_tree(tree, players)
        deck = tree.insert(parent, "end", text="Deck: " + str(len(self.deck)) + " cards")
        for c in self.deck:
            c.make_tree(tree, deck)

    def serialize(self):
        """ Produce a serialized representation of a Dealer according to the specification
        :return: An array of [LOP+, Natural, LOC]
        """
        return [[p.serialize() for p in self.players], self.watering_hole, [c.serialize() for c in self.deck]]

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

                 # Insert the line below when asking players for their choice of species is enabled.
                 # first_player.automatically_choose_species_to_feed(rest_players) or \
        intent = first_player.next_species_to_feed(rest_players, self.watering_hole)

        intent.enact(first_player, rest_players, self)

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

        for feeding in range(feed_amount):
            if not (species.is_hungry() and self.watering_hole):
                return None

            species.food += 1
            self.watering_hole -= 1

        for feeding in range(feed_amount):
            if species.has_trait(Trait.COOPERATION):
                right = player.get_neighbors(species)[1]
                if right:
                    self.feed_creature(player, species_index+1)

        if scavenge:
            idx = self.players.index(player)
            for i in range(len(self.players)):
                player = self.players[(idx+i) % len(self.players)]
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

    def kill_creature(self, player, species_index):
        """ Remove the specified creature from the given player, and move two cards into the player's hand from the deck
        :param player: a Player on which the creature is located
        :param species_index: Integer representing the index of the Species in player's list of Species
        """
        player.species.pop(species_index)
        for i in range(DEAD_CREATURE_REPLACEMENT_CARDS):
            if self.deck:
                player.cards.append(self.deck.pop(0))
