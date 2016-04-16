from unittest import TestCase, mock
from .dealer import Dealer
from .player import Player, InternalPlayer, ExternalPlayer
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
        self.species_fat_food = Species(food=1, population=TINY, body=BIG_SIZE, traits=[Trait.COOPERATION])

        self.attackPlayer = Player(1, species=[self.species_big_car, self.species_small_veg, self.species_tiny_car], bag=5)
        self.scavengingAttackerPlayer = Player(1, species=[self.species_attacker_scavenger], bag=3)
        self.defendPlayer = Player(2, species=[self.species_small_car, self.species_big_veg], bag=2)
        self.hornDefendPlayer = Player(3, species=[self.species_horn_veg], cards=[TraitCard(-3, Trait("long-neck"))])
        self.cooperatingPlayer = Player(4, species=[self.species_cooperating_scavenger, self.species_hungry_forrager])
        self.fatPlayer = Player(5, species=[self.species_fat_food], bag=1)

        self.dealer1 = Dealer([self.attackPlayer, self.defendPlayer, self.hornDefendPlayer, self.cooperatingPlayer],
                              10, [])
        self.dealer3 = Dealer([self.scavengingAttackerPlayer, self.defendPlayer, self.cooperatingPlayer],
                              10, [TraitCard(-3, Trait("long-neck"))])

        self.dealer4 = Dealer([self.scavengingAttackerPlayer, self.defendPlayer, self.hornDefendPlayer],
                              10, [TraitCard(-3, Trait("long-neck")), TraitCard(-3, Trait("carnivore"))])

        self.dealer5 = Dealer([self.hornDefendPlayer, self.scavengingAttackerPlayer, self.defendPlayer], 0,
                                [TraitCard(-3, Trait("long-neck")), TraitCard(-3, Trait("carnivore"))])

        self.dealer6 = Dealer([self.fatPlayer, self.scavengingAttackerPlayer, self.defendPlayer, self.hornDefendPlayer,
                               self.attackPlayer], 0, [TraitCard(-3, Trait("long-neck")), TraitCard(-3, Trait("carnivore"))])
        self.ianpmock = ExternalPlayer(0)
        self.i_att_player = InternalPlayer(0, self.ianpmock)
        self.i_att_player.rehydrate(self.attackPlayer.serialize())

        self.scatmock = ExternalPlayer(1)
        self.i_scav_att_player = InternalPlayer(1, self.scatmock)
        self.i_scav_att_player.rehydrate(self.scavengingAttackerPlayer.serialize())

        self.defendmock = ExternalPlayer(2)
        self.int_def_player = InternalPlayer(2, self.defendmock)
        self.int_def_player.rehydrate(self.defendPlayer.serialize())

        self.hornmock = ExternalPlayer(3)
        self.int_horn_player = InternalPlayer(3, self.hornmock)
        self.int_horn_player.rehydrate(self.hornDefendPlayer.serialize())

        self.coopmock = ExternalPlayer(4)
        self.i_coop_player = InternalPlayer(4, self.coopmock)
        self.i_coop_player.rehydrate(self.cooperatingPlayer.serialize())

        self.ndealer = Dealer([self.i_att_player, self.int_def_player, self.int_horn_player, self.i_coop_player],
                              10, [])

        self.ndealer2 = Dealer([self.i_scav_att_player, self.int_def_player, self.i_coop_player],
                              10, [TraitCard(-3, Trait("long-neck"))])


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
        self.ndealer.feed_one(self.ndealer.players)
        # self.assertEqual(self.species_small_veg.food, 1)
        self.assertEqual(self.ndealer.watering_hole, 9)

        self.dealer1.feed_one(self.ndealer.players)
        # TODO: Fix these so they work despite the new arch— see feed one below for an example
        #self.assertEqual(self.species_small_veg.food, 1)
        #self.assertEqual(self.species_big_car.food, 2)
        #self.assertEqual(self.species_big_veg.population, 3)
        #self.assertEqual(self.species_cooperating_scavenger.food, 2)
        #self.assertEqual(self.species_hungry_forrager.food, 3)
        #self.assertEqual(self.dealer1.watering_hole, 5)

    def test_feed_one_v2(self):
        self.ndealer2.feed_one(self.ndealer2.players)
        self.assertEqual(self.i_scav_att_player.species[0].food, 5)

    def test_fat_feed(self):
        fat_species = Species(food=1, population=BIG_SIZE, body=BIG_SIZE, traits=[Trait.FAT_TISSUE])
        fat_food_player = Player(5, species=[fat_species])
        self.dealer1.fat_feed(fat_food_player, 0, BIG_SIZE)

        self.assertEqual(self.dealer1.watering_hole, 10-BIG_SIZE)
        self.assertEqual(fat_species.fat_food, BIG_SIZE)

    def generate_json_case(self, case_number, dealer):
        """ Generates a pair of json files called {case_number}-in.json and {case_number}-out.json
        """
        in_data = dealer.serialize()
        dealer.feed_one(dealer.players)
        out_data = dealer.serialize()

        directory = os.path.dirname(os.path.realpath(__file__))
        test_directory = os.path.join(directory, "..", "test")
        in_name = "{}-in.json".format(case_number)
        out_name = "{}-out.json".format(case_number)

        in_path = os.path.join(test_directory, in_name)
        out_path = os.path.join(test_directory, out_name)

        print(in_data)
        with open(in_path, "w") as in_file:
            json.dump(in_data, in_file, indent=5)
            in_file.write("\n")
        print(out_data)
        with open(out_path, "w") as out_file:
            json.dump(out_data, out_file)
            out_file.write("\n")

    def generate_xfeed_cases(self):
        """ Generates test cases by serializing cases. Note that because it does so by reserializing,
        it is only testing xfeed, not the entirety of the system— if there is a bug in the dealer, it will propogate.
        """
        test_cases = [self.dealer1, self.dealer3, self.dealer4, self.dealer5, self.dealer6]
        for case_number, situation in enumerate(test_cases):
            self.generate_json_case(case_number + 1, situation)

if __name__ == "__main__":
    dtc = DealerTestCase()
    dtc.setUp()
    dtc.generate_xfeed_cases()