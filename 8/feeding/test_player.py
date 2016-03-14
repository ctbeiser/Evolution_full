import os
import json

from unittest import TestCase

from .species import Species
from .trait import Trait
from .player import Player
from .feeding_intent import FeedNone, FeedVegetarian, StoreFat, FeedCarnivore, CannotFeed
from dealer.traitcard import TraitCard

class PlayerTestCase(TestCase):

    DEFAULT_WATERING_HOLE = 0

    def setUp(self):
        self.species_fed_veg = Species(food=3, population=3)
        self.species_fed_car = Species(food=2, population=2, traits=[Trait.CARNIVORE])
        self.species_fed_fat = Species(food=2, population=2, body=1, traits=[Trait.FAT_TISSUE], fat_food=1)

        self.species_veg_0 = Species(food=0, population=2, body=0)
        self.species_veg_1 = Species(food=0, population=2, body=1)
        self.species_veg_2 = Species(food=1, population=2, body=0)
        self.species_veg_3 = Species(food=0, population=1, body=0)
        self.species_veg_4 = Species(food=0, population=1, body=0)

        self.species_fat_0 = Species(food=0, population=2, body=1, traits=[Trait.FAT_TISSUE], fat_food=0)
        self.species_fat_1 = Species(food=0, population=2, body=2, traits=[Trait.FAT_TISSUE], fat_food=0)

        self.species_car_0 = Species(food=0, population=2, body=0, traits=[Trait.CARNIVORE])
        self.species_car_1 = Species(food=0, population=2, body=1, traits=[Trait.CARNIVORE])
        self.species_car_2 = Species(food=1, population=2, body=0, traits=[Trait.CARNIVORE])
        self.species_car_3 = Species(food=0, population=1, body=0, traits=[Trait.CARNIVORE])
        self.species_car_4 = Species(food=0, population=1, body=0, traits=[Trait.CARNIVORE])

        self.species_defends = Species(food=0, population=1, body=0, traits=[Trait.WARNING_CALL, Trait.HARD_SHELL])
        self.species_easy_target = Species(food=0, population=1, body=0)

    def test_de_serialize(self):

        player_data_values = [
            (1, [], 0),
            (4, [], 4),
            (4, [self.species_fed_veg.serialize()], 4),
            (4, [self.species_fed_veg.serialize(), self.species_fed_fat.serialize()], 4),
            (4, [self.species_fed_veg.serialize(), self.species_fed_fat.serialize()], 4),
        ]
        for pid, species, bag in player_data_values:
            data = [["id", pid], ["species", species], ["bag", bag]]

            player = Player.deserialize(data)
            self.assertIsInstance(player, Player)
            self.assertEqual(player.player_id, pid)
            self.assertEqual(player.bag, bag)
            self.assertCountEqual(player.cards, [])

            for species_obj, species_data in zip(player.species, species):

                self.assertEqual(species_obj.serialize(), species_data)

            self.assertEqual(player.serialize(), data)

            cards = [TraitCard(1, Trait("carnivore")), TraitCard(1, Trait("carnivore"))]
            card_data = [c.serialize() for c in cards]

            data.append(["cards", card_data])

            player = Player.deserialize(data)
            self.assertIsInstance(player, Player)
            self.assertEqual(player.player_id, pid)
            self.assertEqual(player.bag, bag)
            self.assertEqual(len(player.cards), len(cards))
            self.assertEqual(player.cards[0].food_value, 1)
            self.assertEqual(player.cards[0].trait, Trait.CARNIVORE)

    def test_order_species(self):

        player = Player(1)
        player.species = []
        self.assertEqual(player.order_species([]), [])

        player.species = [self.species_veg_1]
        self.assertEqual(player.order_species([]), [])
        self.assertEqual(player.order_species([self.species_veg_1]), [self.species_veg_1])

        # population, 3.pop < 1.pop
        player.species = [self.species_veg_3, self.species_veg_1]
        self.assertEqual(player.order_species([self.species_veg_1, self.species_veg_3]),
                         [self.species_veg_1, self.species_veg_3])

        # food, 2.food > 1.food
        player.species = [self.species_veg_2, self.species_veg_1]
        self.assertEqual(player.order_species([self.species_veg_1, self.species_veg_2]),
                         [self.species_veg_2, self.species_veg_1])

        # body, 0.body < 1.body
        player.species = [self.species_veg_1, self.species_veg_0]
        self.assertEqual(player.order_species([self.species_veg_1, self.species_veg_0]),
                         [self.species_veg_1, self.species_veg_0])

        # board order , 4 is left of 3
        player.species = [self.species_veg_4, self.species_veg_3]
        self.assertEqual(player.order_species([self.species_veg_3, self.species_veg_4]),
                         [self.species_veg_4, self.species_veg_3])

        # everything: 2, 1, 0, 3, 4
        player.species = [self.species_veg_0, self.species_veg_1, self.species_veg_2,
                          self.species_veg_3, self.species_veg_4]
        expected = [self.species_veg_2, self.species_veg_1, self.species_veg_0,
                    self.species_veg_3, self.species_veg_4]

        self.assertEqual(player.order_species(player.species), expected)

        # test subsets
        self.assertEqual(player.order_species([self.species_veg_1, self.species_veg_3]),
                         [self.species_veg_1, self.species_veg_3])
        self.assertEqual(player.order_species([self.species_veg_1, self.species_veg_0]),
                         [self.species_veg_1, self.species_veg_0])

    def test_get_attackable_species(self):

        attacker = Species(traits=[Trait.CARNIVORE])
        defender = Species(traits=[Trait.SYMBIOSIS])

        player = Player(1)
        player.species = [defender]
        result = player.get_attackable_species(attacker)
        self.assertEqual(result, [defender])

        defender1 = Species(traits=[Trait.CLIMBING])
        defender2 = Species(traits=[Trait.SYMBIOSIS])
        defender3 = Species(body=defender2.body + 1, traits=[])

        player.species = [defender1, defender2, defender3]
        result = player.get_attackable_species(attacker)
        self.assertEqual(result, [defender3])

    def test_next_species_to_feed_none(self):

        # player would have to attack their own species
        player = Player(1, species=[self.species_car_0, self.species_fed_veg])
        self.assertIsInstance(player.next_species_to_feed([], self.DEFAULT_WATERING_HOLE), FeedNone)

    def test_next_species_to_feed_cannot_feed(self):

        # no species to feed
        player = Player(1)
        self.assertIsInstance(player.next_species_to_feed([], self.DEFAULT_WATERING_HOLE), CannotFeed)

        # all species fully fed
        player = Player(1, species=[self.species_fed_veg, self.species_fed_car])
        self.assertIsInstance(player.next_species_to_feed([], self.DEFAULT_WATERING_HOLE), CannotFeed)

    def test_next_species_to_feed_vegetarian(self):

        player = Player(1)

        # no species to feed
        player.species = []
        self.assertIsNone(player.feed_vegetarian())

        # no vegetarian species
        player.species = [self.species_car_0, self.species_car_1]
        self.assertIsNone(player.feed_vegetarian())

        # vegetarian species fed
        player.species = [self.species_fed_veg, self.species_car_0, self.species_car_1]
        self.assertIsNone(player.feed_vegetarian())

        # one species to feed
        player.species = [self.species_veg_0, self.species_car_0]
        feeding = player.feed_vegetarian()
        self.assertIsInstance(feeding, FeedVegetarian)
        self.assertEqual(feeding.species_index, player.species.index(self.species_veg_0))

        # choose largest species
        # correct order is 2, 1, 0, 3, 4
        player.species = [self.species_veg_0, self.species_veg_1, self.species_veg_2,
                          self.species_veg_3, self.species_veg_4]
        feeding = player.feed_vegetarian()
        self.assertIsInstance(feeding, FeedVegetarian)
        self.assertEqual(feeding.species_index, player.species.index(self.species_veg_2))

    def test_next_species_to_feed_fat_tissue(self):

        player = Player(1)

        # no species to feed
        player.species = []
        self.assertIsNone(player.feed_fat_tissue(self.DEFAULT_WATERING_HOLE))

        # no fat tissue species
        player.species = [self.species_veg_0, self.species_car_1]
        self.assertIsNone(player.feed_fat_tissue(self.DEFAULT_WATERING_HOLE))

        # species with fat tissue fed
        player.species = [self.species_fed_fat]
        self.assertIsNone(player.feed_fat_tissue(10))

        # one fat tissue species to feed
        player.species = [self.species_fat_0, self.species_veg_1]
        feeding = player.feed_fat_tissue(10)
        self.assertIsInstance(feeding, StoreFat)
        self.assertEqual(feeding.species_index, player.species.index(self.species_fat_0))
        self.assertEqual(feeding.tokens, self.species_fat_0.body - self.species_fat_0.fat_food)
        self.assertGreater(self.species_fat_0.body - self.species_fat_0.fat_food, 0)

        # fat_1 has priority before fat_0, can store more tokens
        player.species = [self.species_fat_0, self.species_fed_car, self.species_fat_1]
        feeding = player.feed_fat_tissue(10)
        self.assertIsInstance(feeding, StoreFat)
        self.assertEqual(feeding.species_index, player.species.index(self.species_fat_1))
        self.assertEqual(feeding.tokens, self.species_fat_1.body - self.species_fat_1.fat_food)
        self.assertGreater(self.species_fat_1.body - self.species_fat_1.fat_food, 0)

        food_available = 1

        player.species = [self.species_fat_0, self.species_fed_car, self.species_fat_1]
        feeding = player.feed_fat_tissue(food_available)
        self.assertIsInstance(feeding, StoreFat)
        self.assertEqual(feeding.species_index, player.species.index(self.species_fat_1))
        self.assertEqual(feeding.tokens, food_available)
        self.assertGreater(self.species_fat_1.body - self.species_fat_1.fat_food, food_available)

    def test_next_species_to_feed_carnivore(self):
        player = Player(1, species=[self.species_car_3, self.species_car_4, self.species_fed_car, self.species_fed_veg])
        enemy1 = Player(2, species=[self.species_veg_1, self.species_veg_0])
        enemy2 = Player(3, species=[self.species_veg_0, self.species_car_1])
        # species_veg_3 is defended by its neighbor
        enemy3 = Player(4, species=[self.species_veg_3, self.species_defends])
        enemy4 = Player(5, species=[self.species_car_1])

        test_cases = [
            ([enemy1], self.species_car_3, enemy1, self.species_veg_1),
            ([enemy2, enemy1], self.species_car_3, enemy2, self.species_car_1),
            ([enemy1, enemy2, enemy3], self.species_car_3, enemy1, self.species_veg_1),
            ([enemy2, enemy4, enemy1], self.species_car_3, enemy2, self.species_car_1),
        ]

        for enemies, attacker, enemy, defender in test_cases:

            expected = FeedCarnivore(
                player.species.index(attacker),
                enemies.index(enemy),
                enemy.species.index(defender)
            )
            result = player.next_species_to_feed(enemies, self.DEFAULT_WATERING_HOLE)

            self.assertIsInstance(result, FeedCarnivore)
            self.assertIs(result.player_index, expected.player_index)
            self.assertIs(result.defender_index, expected.defender_index)
            self.assertIs(result.species_index, expected.species_index)

    def test_get_neighbors(self):
        player = Player(1, species=[self.species_car_0, self.species_car_1, self.species_car_2])

        self.assertEqual(player.get_neighbors(self.species_car_0), (None, self.species_car_1))
        self.assertEqual(player.get_neighbors(self.species_car_1), (self.species_car_0, self.species_car_2))
        self.assertEqual(player.get_neighbors(self.species_car_2), (self.species_car_1, None))

        player2 = Player(1, species=[self.species_car_0, self.species_car_1])
        self.assertEqual(player2.get_neighbors(self.species_car_0), (None, self.species_car_1))
        self.assertEqual(player2.get_neighbors(self.species_car_1), (self.species_car_0, None))

    def test_find_max_values(self):
        self.assertEqual(Player._find_max_values([5, 7, 999, 8, 999], lambda x: x), [999, 999])
        self.assertEqual(Player._find_max_values([5, 7, 999, 8], lambda x: x), [999])
        self.assertEqual(Player._find_max_values([5, 7, 999, 8, 5], lambda x: 0-x), [5, 5])

    @staticmethod
    def generate_json_case(case_number, player, watering_hole, other_players, expected_result):
        """ Generates a pair of json files called {case_number}-in.json and {case_number}-out.json
        """
        in_data = [player.serialize(), watering_hole, [p.serialize() for p in other_players]]
        out_data = expected_result.serialize() if hasattr(expected_result, "serialize") else expected_result

        directory = os.path.dirname(os.path.realpath(__file__))
        test_directory = os.path.join(directory, "..", "test")
        in_name = "{}-in.json".format(case_number)
        out_name = "{}-out.json".format(case_number)

        in_path = os.path.join(test_directory, in_name)
        out_path = os.path.join(test_directory, out_name)

        with open(in_path, "w") as in_file:
            json.dump(in_data, in_file, indent=5)
            in_file.write("\n")
        with open(out_path, "w") as out_file:
            json.dump(out_data, out_file)
            out_file.write("\n")

    def generate_xfeed_cases(self):

        enemy1 = Player(2, species=[self.species_veg_1, self.species_veg_0])

        test_cases = [
            # no species to feed
            (
                Player(1, species=[]),
                1,
                [Player(2, species=[self.species_easy_target]),
                 Player(3, species=[self.species_easy_target])],
                False
            ),
            # all species are fed
            (
                Player(1, species=[self.species_fed_veg, self.species_fed_fat, self.species_fed_car]),
                1,
                [Player(2, species=[self.species_easy_target]),
                 Player(3, species=[self.species_easy_target])],
                False
            ),
            # feed vegetarian
            (
                Player(1, species=[self.species_veg_0, self.species_fed_fat, self.species_fed_car]),
                1,
                [Player(2, species=[self.species_easy_target]),
                 Player(3, species=[self.species_easy_target])],
                FeedVegetarian(0),
            ),
            # feed fat tissue
             (
                Player(1, species=[self.species_veg_0, self.species_fat_1, self.species_fed_car]),
                1,
                [Player(2, species=[self.species_easy_target]),
                 Player(3, species=[self.species_easy_target])],
                StoreFat(1, self.species_fat_1.body - self.species_fat_1.fat_food),
            ),
            # feed carnivore
            (
                Player(1, species=[self.species_car_3, self.species_car_4, self.species_fed_car, self.species_fed_veg]),
                4,
                [
                    enemy1,
                    Player(4, species=[self.species_veg_3, self.species_defends]),
                    Player(3, species=[self.species_veg_0, self.species_car_1]),
                ],
                FeedCarnivore(0, 0, enemy1.species.index(self.species_veg_1)),
            ),
        ]

        for case_number, (player, watering_hole, other_players, expected) in enumerate(test_cases):
            self.generate_json_case(case_number + 1, player, watering_hole, other_players, expected)


if __name__ == "__main__":
    ptc = PlayerTestCase()
    ptc.setUp()
    ptc.generate_xfeed_cases()