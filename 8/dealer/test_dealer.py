from unittest import TestCase, mock
from .dealer import Dealer
from .player import Player
from .species import Species
from .trait import Trait
from .traitcard import TraitCard
import os
import json

BIG_SIZE = 4
LITTLE_SIZE = 2
TINY = 1


class DealerTestCase(TestCase):

    def setUp(self):
        self.species_big_car = Species(food=1, population=BIG_SIZE, body=1, traits=[Trait.CARNIVORE])
        self.species_small_car = Species(food=1, population=LITTLE_SIZE, body=1, traits=[Trait.CARNIVORE])
        self.species_big_veg = Species(food=1, population=BIG_SIZE, body=1, traits=[])
        self.species_small_veg = Species(food=1, population=LITTLE_SIZE, body=1, traits=[])
        self.species_horn_veg = Species(food=1, population=LITTLE_SIZE, body=1, traits=[Trait.HORNS])
        self.species_tiny_car = Species(food=0, population=TINY, body=1, traits=[Trait.CARNIVORE])

        self.species_full_cooperate = Species(food=1, population=TINY, body=1, traits=[Trait.COOPERATION])
        self.species_hungry_forrager = Species(food=1, population=BIG_SIZE, body=1, traits= [Trait.FORAGING])
        self.species_cooperating_scavenger = Species(food=1, population=BIG_SIZE, body=1, traits=[Trait.SCAVENGER, Trait.COOPERATION])
        self.species_attacker_scavenger = Species(food=1, population=8, body=1, traits=[Trait.SCAVENGER, Trait.CARNIVORE, Trait.FORAGING])

        self.attackPlayer = Player(1, species=[self.species_big_car, self.species_small_veg, self.species_tiny_car], bag=5)
        self.scavengingAttackerPlayer = Player(1, species=[self.species_attacker_scavenger], bag=3)
        self.defendPlayer = Player(2, species=[self.species_small_car, self.species_big_veg], bag=2)
        self.hornDefendPlayer = Player(3, species=[self.species_horn_veg], cards=[TraitCard(-5, Trait("long-neck")),
                                                                                  TraitCard(-5, Trait("carnivore")),
                                                                                  TraitCard(0, Trait("long-neck"))])
        self.cooperatingPlayer = Player(4, species=[self.species_cooperating_scavenger, self.species_hungry_forrager])

        self.dealer1 = Dealer([self.attackPlayer, self.defendPlayer, self.hornDefendPlayer, self.cooperatingPlayer],
                              10, [])
        self.dealer3 = Dealer([self.scavengingAttackerPlayer, self.defendPlayer, self.cooperatingPlayer],
                              10, [TraitCard(-5, "long-neck"), TraitCard(-5, "carnivore"), TraitCard(0, "long-neck")])

        self.dealer1_in = Dealer([self.attackPlayer, self.defendPlayer, self.hornDefendPlayer, self.cooperatingPlayer], 10, [])
        self.species_small_veg.food = 2;
        self.dealer1_out = Dealer([self.attackPlayer, self.defendPlayer, self.hornDefendPlayer, self.cooperatingPlayer], 9, [])

        self.dealer2_in = Dealer([self.hornDefendPlayer, self.defendPlayer, self.attackPlayer], 0, [])
        self.dealer2_out = Dealer([self.hornDefendPlayer, self.defendPlayer, self.attackPlayer], 0, [])

        self.dealer3_in = Dealer([self.cooperatingPlayer, self.defendPlayer, self.hornDefendPlayer], 3, [])
        self.species_cooperating_scavenger.food = 2;
        self.species_hungry_forrager.food = 3;
        self.dealer3_out = Dealer([self.cooperatingPlayer, self.defendPlayer, self.hornDefendPlayer], 0, [])

    def test_feed_creature(self):
        self.dealer1.feed_creature(self.attackPlayer, self.attackPlayer.species.index(self.species_big_car),
                                   scavenge=False)
        self.assertEqual(self.species_big_car.food, 1+1)

    def test_serialize(self):
        self.assertEqual(self.dealer1.serialize(), [[self.attackPlayer.serialize(), self.defendPlayer.serialize(),
                                                     self.hornDefendPlayer.serialize(), self.cooperatingPlayer.serialize()], 10, []])

    def test_deserialize(self):
        dealer2 = Dealer.deserialize([[self.attackPlayer.serialize(), self.defendPlayer.serialize(),
                                       self.hornDefendPlayer.serialize(), self.cooperatingPlayer.serialize()], 10, []])
        for p in range(len(self.dealer1.players)):
            self.assertEqual(self.dealer1.players[p].player_id, dealer2.players[p].player_id)
            self.assertEqual(len(self.dealer1.players[p].species), len(dealer2.players[p].species))
            self.assertEqual(self.dealer1.players[p].bag, dealer2.players[p].bag)
            for idx in range(len(self.dealer1.players[p].cards)):
                self.assertEqual(self.dealer1.players[p].cards[idx].serialize(), dealer2.players[p].cards[idx].serialize())
        self.assertEqual(self.dealer1.watering_hole, dealer2.watering_hole)
        self.assertEqual(self.dealer1.deck, dealer2.deck)

    def test_feed_one(self):
        self.dealer1.feed_one(self.dealer1.players)
        self.assertEqual(self.species_small_veg.food, 2)
        #self.assertEqual(self.dealer1.watering_hole, 9)

        self.dealer1.feed_one(self.dealer1.players)
        self.assertEqual(self.species_small_veg.food, 2)
        self.assertEqual(self.species_big_car.food, 2)
        self.assertEqual(self.species_big_veg.population, 3)
        self.assertEqual(self.species_cooperating_scavenger.food, 2)
        self.assertEqual(self.species_hungry_forrager.food, 3)
        self.assertEqual(self.dealer1.watering_hole, 5)

    def test_feed_one_v2(self):
        self.dealer3.feed_one(self.dealer3.players)
        self.assertEqual(self.species_attacker_scavenger.food, 5)

    def test_fat_feed(self):
        fat_species = Species(food=1, population=BIG_SIZE, body=BIG_SIZE, traits=[Trait.FAT_TISSUE])
        fat_food_player = Player(5, species=[fat_species])
        self.dealer1.fat_feed(fat_food_player, 0, BIG_SIZE)

        self.assertEqual(self.dealer1.watering_hole, 10-BIG_SIZE)
        self.assertEqual(fat_species.fat_food, BIG_SIZE)


    def generate_json_case(self, case_number, dealer, expected):
        """ Generates a pair of json files called {case_number}-in.json and {case_number}-out.json
        """
        in_data = dealer.serialize()
        print(in_data)
        out_data = expected.serialize() if hasattr(expected, "serialize") else expected

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
        """
        :return:
        """
        test_cases = [(self.dealer1_in , self.dealer1_out),
                      (self.dealer2_in , self.dealer2_out),
                      (self.dealer3_in , self.dealer3_out)]
        for case_number, (situation, expected) in enumerate(test_cases):
            self.generate_json_case(case_number + 1, situation, expected)

if __name__ == "__main__":
    dtc = DealerTestCase()
    dtc.setUp()
    dtc.generate_xfeed_cases()