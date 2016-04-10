from .trait import Trait
from .player import Player, InternalPlayer
from .traitcard import TraitCard
from .species import Species

DEAD_CREATURE_REPLACEMENT_CARDS = 2
CARD_DRAW_COUNT = 3

class Dealer:
    """
    Represents a Dealer in the game of Evolution.
    """
    def __init__(self, players=None, watering_hole=0, deck=None):
        """ Initialize a new Dealer
        :param players: A list of Player
        :param watering_hole: Integer
        :param deck: List of Trait_Card
        :return:
        """
        self.players = players or []
        self.watering_hole = watering_hole or 0
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

    def play_game(self, external_players):
        if not self.deck:
            self.deck = TraitCard.new_deck()
            self.deck.sort()
        for i, player in enumerate(external_players):
            self.players.append(InternalPlayer(i, player))
        self.step_one()
        actions = self.step_two_and_three()
        self.step_four(actions)

    def step_one(self):
        """
        Carries out Step 1 of the Evolution game
        """
        for player in self.players:
            species_count = len(player.species)
            board = Species() if not species_count else None
            cards = [self.deck.pop() for _ in range(CARD_DRAW_COUNT + species_count)]
            player.add_cards(board, cards)

    def step_two_and_three(self):
        """ Carries out steps 2 and 3 of the evolution game, and returns the actions.
        :return: an List of Action4
        """
        return [p.request_actions(self.players) for p in self.players]

    def step_four(self, action4s):
        """ Carry out Step4 of the Evolution Game, inlcuding applying actions and
        :param action4s: a List of Action4s, of length equal to the list of Players in this Dealer.
        """
        assert(len(action4s) == len(self.players))
        action_players = zip(action4s, self.players)
        for actions, player in action_players:
            if not actions.verify(player):
                assert(False)
            else:
                actions.enact(player)

        self.feeding()

    def feeding(self):
        # The dealer turns over the food cards placed at the watering hole. <- Oops, where do we put those cards???
        # Doing so adds or subtracts food tokens as specified on the trait cards to the pool of tokens available on the watering hole board;
        # the food supply does not go below 0.
        # It also activates the auto-feeding trait cards that players have associated with their species; the food is taken from the watering hole.
        """Beginning with the current starting player, the players feed their species one animal at a time in a round-robin fashion:
A vegetarian species is fed one token from the watering hole supply.

A Carnvivore species must is directed to successfully attack some other species, including a species of the same player, or die. The attack adds a food token to the Carnivores’ species board and reduces the population size of the attacked species by one. The player may direct the attack against a different species for each feeding round.

The acquired food tokens are temporarily stored with the species board. A food token cannot be added if it takes the total beyond the population count. Either of these actions may trigger additional "induced" feedings, depending on the traits associated with currently existing species, including those of others, currently passive players.
The feeding procedure continues until every species board has consumed as many food tokens as there are members of the population, or there is no more food on the watering hole board. All left-over food tokens remain on the watering hole board.

At the end of a turn, the players reduce the population size of each species to the number of food tokens associated with its species board. If a species’ population goes to zero, it becomes extinct. The cards associated with an extinct species are discarded and the player receives two trait cards in return. Finally, the players move all food tokens from all their species boards to their food bags.
"""

    def feed_one(self, players_feeding):
        """ Perform one round of feeding
        :param players_feeding: List of Players, with first to feed at the front
        """
        first_player = players_feeding[0]
        rest_players = [p for p in self.players if p is not first_player]

        intent = first_player.automatically_choose_species_to_feed(rest_players) or \
                first_player.feed_next(self.watering_hole, rest_players)

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

    def get_scores(self):
        results = []
        for player in self.players:
            player_score = player.get_score(), player.player_id
            results.append(player_score)
        results.sort()
        return results
