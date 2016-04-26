from unittest import TestCase, mock

from .trait import Trait
from .traitcard import TraitCard


class TraitTestCase(TestCase):

    def test_trait_order(self):
        self.assertEqual((Trait.CARNIVORE < Trait.AMBUSH), False)
        self.assertEqual((Trait.CARNIVORE > Trait.AMBUSH), True)

    def test_traitcard_order(self):
        self.assertEqual((TraitCard(0, Trait.CARNIVORE) < TraitCard(0, Trait.AMBUSH)), False)
        self.assertEqual((TraitCard(-1, Trait.CARNIVORE) < TraitCard(0, Trait.AMBUSH)), False)
        self.assertEqual((TraitCard(-1, Trait.CARNIVORE) < TraitCard(0, Trait.CARNIVORE)), True)
        self.assertEqual((TraitCard(-1, Trait.AMBUSH) < TraitCard(0, Trait.CARNIVORE)), True)
        self.assertEqual((TraitCard(-1, Trait.AMBUSH) < TraitCard(-1, Trait.SCAVENGER)), True)