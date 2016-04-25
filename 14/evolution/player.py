""" Represents a Player for the Evolution game
"""

from .trait import Trait
from .species import Species
from .feeding_intent import FeedNone, StoreFat, FeedVegetarian, FeedCarnivore, CannotFeed, FeedingIntent
from .traitcard import TraitCard
from .action4 import Action4
from .action import *
from .debug import *

DEFAULT_BAG_VALUE = 0
BAG_JSON_NAME = "bag"
CARDS_JSON_NAME = "cards"


class Player:
    def __init__(self, player_id, species=None, bag=DEFAULT_BAG_VALUE, cards=None):
        """ Initialize a new Player
        :param player_id: id of the player as a Natural number greater than 0
        :param species: a list of Species or None
        :param bag: number of food tokens in the bag
        :param cards: a list of TraitCards that form the player's hand
        """
        self.player_id = player_id
        self.species = species or []
        self.bag = bag
        self.cards = cards or []

    def make_tree(self, tree, parent):
        """ Modify the ttk tree provided to add a representation of this data structure
        :param tree: a ttk Treeview widget object
        :param parent: the ttk reference to a row in the ttk Treeview under which this content should be added.
        """
        p = tree.insert(parent, 'end', text=("Player " + str(self.player_id)))
        tree.insert(p, 'end', text=("Bag:", str(self.bag)))
        for species in self.species:
            species.make_tree(tree, p)

        h = tree.insert(p, 'end', text="Hand: " + ((str(len(self.cards)) + " cards") if self.cards else "empty"))
        for card in self.cards:
            card.make_tree(tree, h)

    def serialize(self):
        """ Returns a serialized version of the Player
        :return: serialized version of the Player
        """
        serialized = [
            ["id", self.player_id],
            ["species", [species.serialize() for species in self.species]],
            [BAG_JSON_NAME, self.bag],
        ]

        if self.cards:
            serialized.append([CARDS_JSON_NAME, [card.serialize() for card in self.cards]])
        return serialized

    def produce_state(self, watering_hole, others=None):
        """ Given a Watering Hole and a list of other players, serializes this Player to a State, as described in the spec
        If others is passed, this will produce a list of 5, starting with the species.
        If others is not passed, it will produce a list of length 4, with the watering hole moved to the front.
        :param watering_hole: Integer
        :param others: List of Player objects, or None
        :return: a Python-encoded JSON Array that encodes the structure of a State
        """
        serialized = [self.bag,
                      [species.serialize() for species in self.species],
                      [card.serialize() for card in self.cards]]
        if others:
            serialized.append(watering_hole)
            serialized.append([p.serialize_species() for p in others])
        else:
            serialized.insert(0, watering_hole)
        return serialized

    def rehydrate_from_state_without_others(self, data):
        """ Sets the content of a Player to match that of JSON representing a State without an associated list of players.
        :param data: JSON representing a State without an associated list of players
        :return Integer representing the watering hole
        Note: This method validates the JSON and ensures that it conforms to the specification.
        If it does not conform, this method will raise a ValueError.
        """
        try:
            if not all([is_list(data),
                        len(data) == 4,
                        is_natural(data[0])]):
                raise ValueError()
        except:
            raise ValueError()

        self.rehydrate_from_state(data[1:])
        return data[0]

    def rehydrate_from_state_with_others(self, data):
        """ Sets the content of a Player to match that of JSON representing a State without an associated list of players.
        :param data: JSON representing a State without an associated list of players
        :return Integer representing the watering hole
        Note: This method validates the JSON and ensures that it conforms to the specification.
        If it does not conform, this method will raise a ValueError.
        """
        try:
            if not all([is_list(data),
                        len(data) == 5,
                        is_natural(data[3]),
                        is_list(data[4])]):
                raise ValueError()
        except:
            raise ValueError()
        self.rehydrate_from_state(data[:3])
        watering_hole = data[3]
        others = [Player.deserialize_species(slist) for slist in data[4]]
        return watering_hole, others

    def rehydrate_from_state(self, data):
        """ Sets the content of a Player to match that of JSON representing a State
        :param data: JSON representing a State
        Note: This method validates the JSON and ensures that it conforms to the specification.
        If it does not conform, this method will raise a ValueError.
        """
        try:
            if not all([is_list(data),
            len(data) == 3,
            is_natural(data[0]),
            is_list(data[1]),
            is_list(data[2])]):
                raise ValueError()
        except ValueError:
            raise ValueError()
        self.bag = data[0]
        try:
            self.species = [Species.deserialize(species) for species in data[1]]
            self.cards = [TraitCard.deserialize(card) for card in data[2]]
        except:
            raise ValueError()

    def rehydrate(self, species=None, bag=None, cards=None):
        if species:
            self.species = species
        if bag:
            self.bag = bag
        if cards:
            self.cards = cards

    def serialize_species(self):
        """ Serialize all species on this player
        :return: python-encoded JSON Array representing a list of Species
        """
        return [s.serialize() for s in self.species]

    @classmethod
    def deserialize_species(cls, data):
        """ Deserializes a Player encoded as a list of Species
        :param data: python encoded JSON array of Species
        :return: Player
        Note: Given an invalid list, this method will raise a ValueError
        """
        if not(is_list(data)):
            raise ValueError()
        return cls(0, species=[Species.deserialize(s) for s in data])

    def rehydrate(self, data):
        """ Sets the fields in this Player from the given JSON representation of one
        :param data:
        """
        self.player_id, self.species, self.bag, self.cards = Player.get_params_from_json(data)

    @classmethod
    def deserialize(cls, data):
        """ Given a serialized representation of the Player according to the evolution spec, produces a Player
        :return: a Player
        """
        return cls(*list(Player.get_params_from_json(data)))

    @staticmethod
    def get_params_from_json(data):
        """ Produces an ordered list of the parameters in a JSON Player
        :param data: JSON representation of a Player
        :return:
        """
        parameters = {parameter: value for parameter, value in data}

        if not 'id' in parameters and 'species' in parameters:
            raise ValueError()

        species = [Species.deserialize(p) for p in parameters['species']]

        cards = []
        if CARDS_JSON_NAME in parameters:
            cards = [TraitCard.deserialize(card) for card in parameters[CARDS_JSON_NAME]]
        bag = None
        if BAG_JSON_NAME in parameters:
            bag = parameters[BAG_JSON_NAME]

        return parameters['id'], species, bag, cards

    @staticmethod
    def _find_max_values(values, key):
        """ Returns a list of maximum values given a key.
        :param values: list of Python values
        :param key: a function of type (Value -> sortable Value)
        :return: a List containing all elements tied for first place according to the given key.
        """
        max_key = max(key(v) for v in values)
        return [v for v in values if key(v) == max_key]

    @staticmethod
    def species_ordering_key(species):
        """ Generates a sorting key for the given species.

          Species are ordered in a lexicographic manner, starting with
           the (plain) population attribute, followed by the food that
           the species has been fed so far, and finally the (plain) body size.

        :param species: a Species to generate a sorting key for
        :return: a Python sorting key for the given species
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

    def get_neighbors(self, species):
        """ Returns the left and right neighbor of the given species.
        :param species: Species to find the neighbors of
        :return: a tuple of (left, right) neighbor, where either can be None
        """
        species_length = len(self.species)

        species_position = self.species.index(species)
        left = self.species[species_position - 1] if species_position > 0 else None
        right = self.species[species_position + 1] if species_position < (species_length - 1) else None

        return left, right

    def get_attackable_species(self, attacker):
        """ Returns all species owned by this player that are attackable by the given species.
        :param attacker: the attacking species
        :return: list of Species attackable by the attacker
        """
        def is_attackable(species):
            left, right = self.get_neighbors(species)
            return species.is_attackable(attacker, left=left, right=right)

        return [species for species in self.species if is_attackable(species)]

    def get_fat_or_hungry_species(self):
        """ Returns a dictionary of string->Array, where each array contains all species which, given the correct board
        state, could produce a feeding action
        :return: Dictionary<String, Array<Species>>
        """
        fat_tissue = [species for species in self.species
                    if species.has_trait(Trait.FAT_TISSUE) and
                        species.fat_food < species.body]
        carnivores = [species for species in self.species
                    if species.has_trait(Trait.CARNIVORE) and
                        species.is_hungry()]
        vegetarians = [species for species in self.species
                    if not species.has_trait(Trait.CARNIVORE) and
                        species.is_hungry()]
        return {"fat": fat_tissue, "carn": carnivores, "veg": vegetarians}

    def get_score(self):
        """ Calculate a score for this player
        :return: Integer representing a score
        """
        score = self.bag
        for species in self.species:
            score += species.population
            score += len(species.traits)
        return score


class InternalPlayer(Player):

    def __init__(self, player_id, external_player, handshake=""):
        """
        :param player_id: Integer representing the ID for this player
        :param external_player: an ExternalPlayer to act as an agent for this player.
        """
        self.player_agent = external_player
        self.handshake = handshake
        super().__init__(player_id)

    def start(self, board, cards, watering_hole):
        """ Add cards and optionally a Species to this player, update the state of the external player.
        :param board: A Species or None
        :param cards: A List of TraitCard
        :param watering_hole: an Integer representing the Watering Hole
        """
        self.cards.extend(cards)
        if board:
            self.species.append(board)
        self.player_agent.start(self.produce_state(watering_hole))

    def request_actions(self, players):
        """ Request an Action4 for this turn from the ExternalPlayer
        :param players: A list of all player objects in this game.
        :return: a new Action4
        """
        location = players.index(self)
        before = [player.serialize_species() for player in players[:location]]
        after = [player.serialize_species() for player in players[location+1:]]
        try:
            actions = Action4.deserialize(self.player_agent.choose(before, after))
            actions.verify(self)
            return actions
        except ValueError:
            return None

    def feed_next(self, watering_hole, players):
        """
        :param watering_hole: an Integer representing the food tokens in the Watering Hole
        :param players: other Players in the game
        :return: a FeedingIntention, or None in the case of an invalid feeding
        """
        feeding = self.automatically_choose_species_to_feed(players)
        if feeding:
            assert (feeding.is_valid(self, players, watering_hole))  # Should never fail, but if it does, we want to know before ship
            return feeding
        else:
            try:
                result = self.player_agent.feed_species(self.produce_state(watering_hole, players))
                feeding = FeedingIntent.deserialize(result)
                if feeding.is_valid(self, players, watering_hole):
                    return feeding
                else:
                    raise ValueError()
            except ValueError as e:
                debug_traceback(e.__traceback__)
                return None

    def automatically_choose_species_to_feed(self, players):
        """ If there's only one possibility, produce an intent that can be automatically carried out by the dealer.
        :param players: A list of all other players
        :return: An FeedingIntent or None, where None represents the situation where there are multiple options.
        """
        options = self.get_fat_or_hungry_species()
        fat, hungry_carnivores, hungry_veg = options["fat"], options["carn"], options["veg"]

        carnivore_targets = [(player.get_attackable_species(candidate), player, candidate) for player in players for candidate in hungry_carnivores]
        if len(carnivore_targets) == 1 and len(carnivore_targets[0][0]) == 1 and not hungry_veg and not fat:
            attackable_species, player, candidate = carnivore_targets[0]
            return FeedCarnivore(self.species.index(carnivore_targets[0][2]),
                                players.index(carnivore_targets[0][1]),
                                player.species.index(attackable_species[0]))
        elif carnivore_targets:
            return None
        elif not fat and not hungry_veg:
            return CannotFeed()

        elif len(hungry_veg) == 1 and not fat:
            return FeedVegetarian(self.species.index(hungry_veg[0]))

    def move_tokens_to_bag(self):
        """ Move food tokens on the creatures into the player's bag.
        :return:
        """
        for s in self.species:
            self.bag += s.food
            s.food = 0

    def starve_creatures(self, kill_species):
        """ Remove creatures with no food and move cards to this player's hand as appropriate.
        :param kill_species: a function that takes this Player and the index of the creature to kill on this player.
        """
        # don't remove creatures from the list while iterating!
        creatures_copy = [s for s in self.species]
        for creature in creatures_copy:
            creature.population = min(creature.population, creature.food)
            if creature.population <= 0:
                kill_species(self, self.species.index(creature))

class ExternalPlayer(Player):

    def choose(self, before, after):
        """ Implement the Silly Strategy for choosing cards, based on the current hand of the Player.
        :param before: players before this one in the list, as a List of JSON Players containing only public info
        :param after: players after this one in the list, as a List of JSON Players containing only public info
        :return: Action4 as JSON, representing choices made
        """
        sorted_cards = [card for card in self.cards]
        sorted_cards.sort()

        foodcard = self.cards.index(sorted_cards.pop(0))

        board_actions, popup, bodyup, replace = [], [], [], []
        if len(sorted_cards) >= 2:
            board_actions = [NewBoardAction(self.cards.index(sorted_cards.pop(0)), [self.cards.index(sorted_cards.pop(0))])]

        if sorted_cards:
            popup = [PopulationUpAction(len(self.species), self.cards.index(sorted_cards.pop(0)))]
        if sorted_cards:
            bodyup = [BodyUpAction(len(self.species), self.cards.index(sorted_cards.pop(0)))]
        if sorted_cards:
            replace = [TraitReplaceAction(len(self.species), 0, self.cards.index(sorted_cards.pop(0)))]

        actions = Action4(foodcard, popup, bodyup, board_actions, replace)
        return actions.serialize()

    def start(self, msg):
        """ Given a JSON message representing a message to start the game, update internal state
            :param msg: a JSON message with a State without others, as described in the spec
        """
        self.rehydrate_from_state_without_others(msg)

    def feed_species(self, state):
        """  Carrys out a single feeding according to the Silly Strategy
        :param state: a State
        :return: A JSON representation of the changed species
        Note: Given an improper input, this function will raise a ValueError.
        """
        wh, players = self.rehydrate_from_state_with_others(state)
        return self.next_species_to_feed(players, wh).serialize()

    def next_species_to_feed(self, players, watering_hole):
        """ Determines the next species to feed, given the other players in the game.
        :param players: list of Player
        :param watering_hole: number of food tokens in the watering hole
        :return: FeedingIntention
        """
        return (self.feed_fat_tissue(watering_hole) or
                self.feed_vegetarian() or
                self.feed_carnivore(players) or
                self.feed_on_own())

    def feed_fat_tissue(self, watering_hole):
        """ Returns an intent to store the specified number of food tokens on the largest species with the "fat tissue"
        trait. If there are no suitable species returns None
        :param watering_hole: number of food tokens in the watering hole
        """
        species_with_fat_tissue = self.get_fat_or_hungry_species()["fat"]
        # greatest need for fat food: the body size of the species
        if len(species_with_fat_tissue) > 0:
            species_with_greatest_need = self._find_max_values(species_with_fat_tissue,
                                                            lambda species: species.body-species.fat_food)

            eater = self.order_species(species_with_greatest_need)[0]
            food_to_request = min(eater.body - eater.fat_food, watering_hole)
            return StoreFat(self.species.index(eater), food_to_request)

    def feed_vegetarian(self):
        """ Returns an intent to feed the largest hungry vegetarian species belonging to this player or None if there
        are no hungry vegetarians.
        :return: A FeedingIntent to feed the largest hungry vegetarian, or None
        """
        vegetarians = self.get_fat_or_hungry_species()["veg"]

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

        :param players: a List of the other players in the game
        :return: a FeedingIntent to attack or None
        """
        carnivores = self.get_fat_or_hungry_species()["carn"]

        eater_candidates = self.order_species(carnivores)
        for candidate in eater_candidates:
            attackable_species = [player.get_attackable_species(candidate) for player in players]
            if any(attackable_species):
                largest_attackable = []
                for player, player_attackable_species in zip(players, attackable_species):
                    if player_attackable_species:
                        player_largest_attackable = player.order_species(player_attackable_species)[0]
                        largest_attackable.append((player_largest_attackable, player))

                def defender_player_key(species_player):
                    """ Sorts defender_player list based on largest species and then player order"""
                    species, player = species_player
                    # The following has been removed for lack of support in the protocol.
                    #player_id = player.player_id
                    #if player_id > self.player_id:
                        #player_id -= 1000
                    return self.species_ordering_key(species), #player_id

                defender, player = sorted(largest_attackable, key=defender_player_key)[0]
                return FeedCarnivore(self.species.index(candidate),players.index(player),player.species.index(defender))

    def feed_on_own(self):
        """ Checks if the player can feed on one of their species. If so
         an intent not to feed will be returned as the Player doesn't want
         to attack their own species.

        :return: FeedingIntent or None
        """
        can_attack_own = self.feed_carnivore([self])
        return FeedNone() if can_attack_own else None


class ProxyPlayer:
    """A Player that follows the interface for an External Player, but connects with an agent across a JSONSocket"""

    def __init__(self, jsock):
        """ Creates a player that acts as an ExternalPlayer, by connecting to it remotely using a StreamingJsonCoder
        :param jsock:
        """
        self.jsock = jsock

    # The following three method's signatures represent the

    def start(self, msg):
        """ Given a JSON message representing a message to start the game, send it to the remote player
        :param msg: a JSON message
        """
        self.jsock.encode(msg)

    def choose(self, before, after):
        """ Ask the remote player to choose the actions to take based on state and the players before and after
        :param before: a list of Player as JSON
        :param after: a list of Player as JSON
        :return: a Action4 as JSON
        Note: This message will raise a ValueError if the agent doesn't conform to the protocol.
        """
        try:
            json_response = self.jsock.send_and_get_response([before, after])
            return json_response
        except ConnectionResetError:
            raise ValueError()

    def feed_species(self, state):
        """ Ask the remote player to feed the species
        :param state: A python-encoded JSON State
        :return: a python-encoded FeedingIntent
        Note: This message will raise a ValueError if the agent doesn't conform to the protocol.
        """
        try:
            maybe_raw_json_response = self.jsock.send_and_get_response(state)
            return maybe_raw_json_response
        except ConnectionResetError:
            raise ValueError()