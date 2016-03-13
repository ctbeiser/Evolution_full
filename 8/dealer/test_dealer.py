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
        self.species_hungry_cooperate = Species(food=1, population=BIG_SIZE, body=1, traits= [Trait.COOPERATION])

        self.attackPlayer = Player(1, species=[self.species_big_car, self.species_small_veg, self.species_tiny_car])
        self.defendPlayer = Player(2, species=[self.species_small_car, self.species_big_veg])
        self.hornDefendPlayer = Player(2, species=[self.species_horn_veg])

        self.dealer1 = Dealer([self.attackPlayer, self.defendPlayer, self.hornDefendPlayer], 10, [])

    def test_feed_creature(self):
        self.dealer1.feed_creature(self.attackPlayer, self.attackPlayer.species.index(self.species_big_car), scavenge=False)
        self.assertEqual(self.species_big_car.food, 1+1)
