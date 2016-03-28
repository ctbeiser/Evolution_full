from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import MagicMock
from player import Player
from species import Species
from trait import Trait
from feeding_intent import FeedCarnivore, FeedVegetarian, StoreFat, CannotFeed, FeedNone
from dealer import Dealer

BIG_SIZE = 4
LITTLE_SIZE = 2
TINY = 1

class FeedingIntentTestCase(TestCase):

    def setUp(self):
        self.species_big_car = Species(food=1, population=BIG_SIZE, body=1, traits=[Trait.CARNIVORE])
        self.species_small_car = Species(food=1, population=LITTLE_SIZE, body=1, traits=[Trait.CARNIVORE])
        self.species_big_veg = Species(food=1, population=BIG_SIZE, body=1, traits=[])
        self.species_small_veg = Species(food=1, population=LITTLE_SIZE, body=1, traits=[])
        self.species_horn_veg = Species(food=1, population=LITTLE_SIZE, body=1, traits=[Trait.HORNS])
        self.species_tiny_car = Species(food=0, population=TINY, body=1, traits=[Trait.CARNIVORE])

        self.attackPlayer = Player(1, species=[self.species_big_car, self.species_small_veg, self.species_tiny_car])
        self.defendPlayer = Player(2, species=[self.species_small_car, self.species_big_veg])
        self.hornDefendPlayer = Player(2, species=[self.species_horn_veg, self.species_big_veg])

    def test_serialize_feed_vegetarian(self):
        for i in range(0, 5):
            veg = FeedVegetarian(i)
            self.assertEqual(veg.serialize(), i)

    def test_enact_vegetarian(self):
        for i in range(0, 5):
            veg = FeedVegetarian(i)
            player = Player(1)
            dealer = Mock()
            dealer.feed_creature = Mock()
            veg.enact(player, False, dealer)
            dealer.feed_creature.assert_called_once_with(player, i)

    def test_enact_carnivore(self):
        player_list = [self.defendPlayer, self.hornDefendPlayer]
        big_veg_intent = FeedCarnivore(self.attackPlayer.species.index(self.species_big_car),
                               player_list.index(self.defendPlayer),
                               self.defendPlayer.species.index(self.species_big_veg))

        mock = Mock()
        mock.feed_creature = MagicMock()
        big_veg_intent.enact(self.attackPlayer, player_list, mock)
        mock.feed_creature.assert_called_once_with(self.attackPlayer, self.attackPlayer.species.index(self.species_big_car), scavenge=True)

        self.assertEqual(self.species_big_car.population, BIG_SIZE)
        self.assertEqual(self.species_big_veg.population, BIG_SIZE-1)
        self.assertIn(self.species_big_car, self.attackPlayer.species)
        self.assertIn(self.species_big_veg, self.defendPlayer.species)

        mock = Mock()
        mock.feed_creature = MagicMock()
        horn_intent = FeedCarnivore(self.attackPlayer.species.index(self.species_big_car),
                               player_list.index(self.hornDefendPlayer),
                               self.hornDefendPlayer.species.index(self.species_horn_veg))

        horn_intent.enact(self.attackPlayer, player_list, mock)

        mock.feed_creature.assert_called_once_with(self.attackPlayer, self.attackPlayer.species.index(self.species_big_car), scavenge=True)

        self.assertEqual(self.species_big_car.population, BIG_SIZE-1)
        self.assertEqual(self.species_horn_veg.population, LITTLE_SIZE-1)
        self.assertIn(self.species_big_car, self.attackPlayer.species)

        tiny_car_dies_intent = FeedCarnivore(self.attackPlayer.species.index(self.species_tiny_car),
                                             player_list.index(self.hornDefendPlayer),
                                             self.hornDefendPlayer.species.index(self.species_horn_veg))

        dealer = Dealer([self.attackPlayer, self.defendPlayer, self.hornDefendPlayer], 10, [])
        dealer.feed_creature = Mock()
        tiny_car_dies_intent.enact(self.attackPlayer, player_list, dealer)

        dealer.feed_creature.assert_not_called()
        self.assertNotIn(self.species_tiny_car, self.attackPlayer.species)
        self.assertNotIn(self.species_horn_veg, self.hornDefendPlayer.species)

    def test_serialize_carnivore(self):
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    self.assertEqual(FeedCarnivore(x, y, z).serialize(), [x, y, z])

    def test_enact_fat_tissue(self):
        for idx in range(0,3):
            for tkns in range(0, 2):
                tissue = StoreFat(idx, tkns)
                mock = Mock()
                mock.feed_creature = Mock()
                player = Mock()
                mock.fat_feed = Mock()
                mock.kill_creature = Mock()
                tissue.enact(player, [], mock)
                mock.kill_creature.assert_not_called()
                mock.feed_creature.assert_not_called()
                mock.fat_feed.assert_called_once_with(player, idx, tkns)

    def test_serialize_fat_tissue(self):
        for x in range(2):
            for y in range(2):
                    self.assertEqual(StoreFat(x, y).serialize(), [x, y])

    def test_cant_feed(self):
        cant_feed = CannotFeed()
        not_called = Mock()
        not_called.feed_creature = Mock()
        not_called.kill_creature = Mock()
        not_called.fat_feed = Mock()
        player = Mock()
        cant_feed.enact(player, [], not_called)
        player.assert_not_called()
        not_called.feed_creature.assert_not_called()
        not_called.kill_creature.assert_not_called()
        not_called.fat_feed.assert_not_called()

    def test_feed_none(self):
        feed_none = FeedNone()
        not_called = Mock()
        not_called.feed_creature = Mock()
        not_called.kill_creature = Mock()
        not_called.fat_feed = Mock()
        player = Mock()
        feed_none.enact(player, [], not_called)
        player.assert_not_called()
        not_called.feed_creature.assert_not_called()
        not_called.kill_creature.assert_not_called()
        not_called.fat_feed.assert_not_called()

    def test_serialize_feed_none(self):
        self.assertEqual(FeedNone().serialize(), False)
