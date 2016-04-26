from .trait import Trait
from .player import Player, InternalPlayer
from .traitcard import TraitCard
from .species import Species
from .debug import debug

DEAD_CREATURE_REPLACEMENT_CARDS = 2
CARD_DRAW_COUNT = 3
MAX_PLAYERS = 8
MIN_PLAYERS = 3

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
        self.watering_hole = watering_hole
        self.deck = deck or []
        self.starting_player = 0

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
        """ Runs the game from the top level
        :param external_players: a List of (ExternalPlayer object, String) representing a player & its handshake, where
        an ExternalPlayer object is described in EXTERNAL_PLAYER_SPEC.md
        """
        if not self.deck:
            self.deck = TraitCard.new_deck()
            self.deck.sort()
        for i, (player, string) in enumerate(external_players, start=1):
            self.players.append(InternalPlayer(i, player, handshake=string))

        while not self.game_over():
            self.step_one()
            actions = self.step_two_and_three()
            self.step_four(actions)

    def game_over(self):
        """ Should the game stop?
        :return: Boolean
        """
        return (not self.players) or \
            sum([CARD_DRAW_COUNT + len(player.species) for player in self.players]) > len(self.deck)

    def step_one(self):
        """
        Carries out Step 1 of the Evolution game
        """
        for player in self.players:
            species_count = len(player.species)
            board = Species() if not species_count else None
            cards = [self.deck.pop() for _ in range(CARD_DRAW_COUNT + max(1, species_count))]
            player.start(board, cards, self.watering_hole)

    def step_two_and_three(self):
        """ Carries out steps 2 and 3 of the evolution game, and returns the actions.
        :return: an List of Action4
        """
        # Local copy so we can modify self.players while iterating
        players = [p for p in self.players]
        requests = [p.request_actions(self.players) for p in self.players]
        for r, p in zip(requests, players):
            if not r:
                self.players.remove(p)
        return [r for r in requests if r]

    def step_four(self, actions):
        """ Carries out Step4 of the feeding process
        :param actions: An Action4 to carry out
        """
        self.apply_actions(actions)
        self.autofeed()
        self.feeding()

    def apply_actions(self, action4s):
        """ Apply Action4s to their players and update the watering hole
        :param action4s: a List of Action4s, of length equal to the list of Players in this Dealer.
        :return: a List of TraitCard to be placed in the watering hole
        """
        watering_hole_cards = []
        action_players = zip(action4s, self.players)
        for actions, player in action_players:
            food_card = actions.enact(player)
            watering_hole_cards.append(food_card.food_value)
        for card in watering_hole_cards:
            self.watering_hole = max(0, self.watering_hole + card)

    def autofeed(self):
        """ Carries out adding population for Fertile, feeding for long_neck, and transferring fat tissue
        """
        for player in self.players:
            for species in player.species:
                species.population += species.has_trait(Trait.FERTILE)
        for player in self.players:
            for species in player.species:
                if species.has_trait(Trait.LONG_NECK):
                    self.feed_creature(player, player.species.index(species))
        for player in self.players:
            for species in player.species:
                if species.has_trait(Trait.FAT_TISSUE) and species.population > species.food and species.fat_food:
                    difference = min(species.fat_food, species.population - species.food)
                    species.fat_food -= difference
                    species.food += difference

    def feeding(self):
        """ Carry out a round of feeding.
        """
        current_player_idx = self.starting_player
        players = [p for p in self.players]
        before = players[:current_player_idx+1]
        ordered_players = players[current_player_idx:] + players[:current_player_idx]

        while (ordered_players and self.watering_hole):
            self.feed_one(ordered_players)

        if self.players:
            # the extra complexity here is necessary in the case we remove players: don't want to lose our spot.
            self.starting_player = (len([player for player in before if player in self.players])-1 + 1) % len(self.players)
        for player in self.players:
            player.starve_creatures(self.kill_creature)
            player.move_tokens_to_bag()

    def feed_one(self, players_feeding):
        """ Perform one round of feeding, and mutates the given Players appropriately, including removing
        :param players_feeding: List of Players, with first to feed at the front
        """
        first_player = players_feeding[0]
        rest_players = [p for p in self.players if p is not first_player]
        intent = first_player.feed_next(self.watering_hole, rest_players)

        if not intent:
            debug("Removed player " + str(self.players.index(first_player)))
            self.players.remove(first_player)
            players_feeding.pop(0)
            return
        else:
            intent.enact(first_player, rest_players, self)

            if intent.should_end_feeding():
                players_feeding.pop(0)
            else:
                players_feeding.append(players_feeding.pop(0))

    def feed_creature(self, player, species_index, scavenge=False):
        """ Feed the creature from the watering hole if possible.
        It is safe to call this method on a full creature.
        :param player: Player on which the species is located
        :param species_index: Integer index of that species on the given Player
        :param scavenge: Boolean indicating whether creatures with scavenger should be fed.
        """
        species = player.species[species_index]
        if not (species.is_hungry() and self.watering_hole):
            return
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
        to_add = []
        for i in range(DEAD_CREATURE_REPLACEMENT_CARDS):
            if self.deck:
                to_add.append(self.deck.pop(0))
        to_add.reverse()
        for card in to_add:
            player.cards.insert(0, card)

    def get_scores(self):
        """ Get all the scores for this game, in sorted order.
        :return: a List(Integer, Integer, String), representing score, player ID, and Handshake respectively.
        """
        results = []
        for player in self.players:
            player_details = player.get_score(), player.player_id, player.handshake
            results.append(player_details)
        results.sort(reverse=True)
        return results
