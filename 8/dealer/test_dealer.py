from unittest import TestCase, mock
from .dealer import Dealer
from feeding.player import Player
from feeding.species import Species
from feeding.trait import Trait

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

        self.attackPlayer = Player(1, species=[self.species_big_car, self.species_small_veg, self.species_tiny_car])
        self.defendPlayer = Player(2, species=[self.species_small_car, self.species_big_veg])
        self.hornDefendPlayer = Player(3, species=[self.species_horn_veg])
        self.cooperatingPlayer = Player(4, species=[self.species_cooperating_scavenger, self.species_hungry_forrager])

        self.dealer1 = Dealer([self.attackPlayer, self.defendPlayer, self.hornDefendPlayer, self.cooperatingPlayer], 10, [])

    def test_feed_creature(self):
        self.dealer1.feed_creature(self.attackPlayer, self.attackPlayer.species.index(self.species_big_car), scavenge=False)
        self.assertEqual(self.species_big_car.food, 1+1)

    def test_serialize(self):
        self.assertEqual(self.dealer1.serialize(), [[self.attackPlayer, self.defendPlayer, self.hornDefendPlayer, self.cooperatingPlayer], 10, []])

    def test_deserialize(self):
        dealer2 = Dealer.deserialize([[self.attackPlayer.serialize(), self.defendPlayer.serialize(), self.hornDefendPlayer.serialize(), self.cooperatingPlayer.serialize()], 10, []])
        for p in range(len(self.dealer1.players)):
            self.assertEqual(self.dealer1.players[p].player_id, dealer2.players[p].player_id)
            self.assertEqual(len(self.dealer1.players[p].species), len(dealer2.players[p].species))
            self.assertEqual(self.dealer1.players[p].bag, dealer2.players[p].bag)
            self.assertEqual(self.dealer1.players[p].cards, dealer2.players[p].cards)
        self.assertEqual(self.dealer1.watering_hole, dealer2.watering_hole)
        self.assertEqual(self.dealer1.deck, dealer2.deck)

    def test_feed_one(self):
        self.dealer1.feed_one(self.dealer1.players)
        self.assertEqual(self.species_small_veg.food, 2)
        self.assertEqual(self.dealer1.watering_hole, 9)

        self.dealer1.feed_one(self.dealer1.players)
        self.assertEqual(self.species_small_veg.food, 2)
        self.assertEqual(self.species_big_car.food, 2)
        self.assertEqual(self.species_big_veg.population, 3)
        self.assertEqual(self.species_cooperating_scavenger.food, 2)
        self.assertEqual(self.species_hungry_forrager.food, 3)
        self.assertEqual(self.dealer1.watering_hole, 5)

    def test_fat_feed(self):
        fat_species = Species(food=1, population=BIG_SIZE, body=BIG_SIZE, traits=[Trait.FAT_TISSUE])
        fat_food_player = Player(5, species=[fat_species])
        self.dealer1.fat_feed(fat_food_player, 0, BIG_SIZE)

        self.assertEqual(self.dealer1.watering_hole, 10-BIG_SIZE)
        self.assertEqual(fat_species.fat_food, BIG_SIZE)

