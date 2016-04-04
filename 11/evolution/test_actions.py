from .dealer import Dealer
from unittest import TestCase, mock
from .action import *
from .trait import *
import json

class UpActionTestCase(TestCase):
    def setUp(self):
        example_config = """[[[["id",2],
  ["species",[[["food",4],
               ["body",4],
               ["population",4],
               ["traits",["fat-tissue"]],
               ["fat-food" ,4]]]],
  ["bag",42],
  ["cards",[[3, "climbing"], [4, "long-neck"]]]],
 [["id",3],
  ["species",[[["food",1],
               ["body",4],
               ["population",4],
               ["traits",["carnivore"]]]]],
  ["bag",2],
  ["cards",[[-3, "burrowing"]]]],
 [["id",4],
  ["species",[[["food",0],
               ["body",7],
               ["population",1],
               ["traits",["fat-tissue"]],
               ["fat-food" ,4]]]],
  ["bag",100],
  ["cards",[[-3, "burrowing"]]]]],
6,
[]]"""
        self.dealer = Dealer.deserialize(json.loads(example_config))

    def test_pop_up(self):
        p = self.dealer.players[0]
        pop_up = PopulationUpAction(0, 1)
        s = p.species[0]
        self.assertEqual(pop_up.cards(), [1])
        self.assertEqual(pop_up.serialize(), PopulationUpAction.deserialize(pop_up.serialize()).serialize())

        pop_up.enact(p)
        self.assertEqual(len(p.species), 1)
        self.assertEqual(p.cards[0].trait, Trait.CLIMBING)
        self.assertEqual(s.population, 5)
        self.assertEqual(s.body, 4)
        self.assertEqual(s.food, 4)

    def test_body_up(self):
        p = self.dealer.players[0]
        b_up = BodyUpAction(0, 1)
        s = p.species[0]
        self.assertEqual(b_up.cards(), [1])
        self.assertEqual(b_up.serialize(), BodyUpAction.deserialize(b_up.serialize()).serialize())

        b_up.enact(p)
        self.assertEqual(len(p.species), 1)
        self.assertEqual(s.population, 4)
        self.assertEqual(s.body, 5)
        self.assertEqual(s.food, 4)

    def test_board_action(self):
        p = self.dealer.players[0]
        self.assertEqual(len(p.cards), 2)
        board = NewBoardAction(0, [1])
        s = p.species[0]
        self.assertEqual(board.cards(), [0, 1])
        self.assertEqual(board.serialize(), NewBoardAction.deserialize(board.serialize()).serialize())

        board.enact(p)
        self.assertEqual(len(p.species), 2)
        self.assertEqual(p.species[1].traits[0], Trait.LONG_NECK)
        self.assertEqual(s.population, 4)
        self.assertEqual(s.body, 4)
        self.assertEqual(s.food, 4)

    def test_replace_action(self):
        p = self.dealer.players[0]
        self.assertEqual(len(p.cards), 2)
        board = TraitReplaceAction(0, 0, 0)
        s = p.species[0]
        self.assertEqual(board.cards(), [0])
        self.assertEqual(board.serialize(), TraitReplaceAction.deserialize(board.serialize()).serialize())

        board.enact(p)
        self.assertEqual(len(p.species), 1)
        self.assertEqual(s.traits[0], Trait.CLIMBING)
        self.assertEqual(s.population, 4)
        self.assertEqual(s.body, 4)
        self.assertEqual(s.food, 4)
        self.assertEqual(len(s.traits), 1)
