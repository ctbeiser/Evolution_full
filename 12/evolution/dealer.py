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
        if not self.deck:
            self.deck = TraitCard.new_deck()
            self.deck.sort()
        for i, player in enumerate(external_players):
            self.players.append(InternalPlayer(i, player))

        while not self.game_over():
            self.step_one()
            actions = self.step_two_and_three()
            self.step_four(actions)

    def game_over(self):
        return sum([CARD_DRAW_COUNT + len(player.species) for player in self.players]) > len(self.deck)

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

    def step_four(self, actions):
        self.apply_actions(actions)
        self.autofeed()
        self.feeding()

    def apply_actions(self, action4s):
        """ Apply Action4s to their players and retrieve t
        :param action4s: a List of Action4s, of length equal to the list of Players in this Dealer.
        :return: a List of TraitCard to be placed in the watering hole
        """
        watering_hole_cards = []
        assert(len(action4s) == len(self.players))
        action_players = zip(action4s, self.players)
        for actions, player in action_players:
            if not actions.verify(player):
                assert(False)
            else:
                food_card = actions.enact(player)
                watering_hole_cards.append(food_card.food_value)
        self.watering_hole = max(0, self.watering_hole + sum(watering_hole_cards))

    def autofeed(self):
        for player in self.players:
            for species in player.species:
                species.population += species.has_trait(Trait.FERTILE)
        for player in self.players:
            for species in player.species:
                if species.has_trait(Trait.LONG_NECK):
                    self.feed_creature(player, player.species.index(species))

    def feeding(self):
        current_player = self.starting_player
        players = [p for p in self.players]
        ordered_players =  players[-current_player:] + players[:-current_player]

        while (ordered_players or self.watering_hole):
            self.feed_one(ordered_players)

        self.starting_player = (self.starting_player + 1) % len(self.players)

        for player in self.players:
            self.move_tokens_to_bag()

    def feed_one(self, players_feeding):
        """ Perform one round of feeding, and mutates the given Players appropriately, including removing
        :param players_feeding: List of Players, with first to feed at the front
        """
        first_player = players_feeding[0]
        rest_players = [p for p in self.players if p is not first_player]

        intent = first_player.automatically_choose_species_to_feed(rest_players) or \
                first_player.feed_next(self.watering_hole, rest_players)

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
