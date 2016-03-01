from unittest import TestCase, mock

from .species import Species
from .trait import Trait, HARD_SHELL_THRESHOLD


class SpeciesTestCase(TestCase):

    def test_to_from_json(self):

        species = Species(food=0, body=1, population=2, traits=[Trait.CARNIVORE])
        species_json = [
            ["food", 0],
            ["body", 1],
            ["population", 2],
            ["traits", [Trait.CARNIVORE.value]],
        ]

        self.assertEqual(species.to_json(), species_json)
        self.assertEqual(species.from_json(species.to_json()).to_json(), species_json)


class SpeciesIsAttackableTestCase(TestCase):

    def test_attacker_carnivore(self):
        # Carnivore

        defender = Species()
        attacker = Species()

        self.assertFalse(defender.is_attackable(attacker))

        attacker.traits = [Trait.CARNIVORE]

        self.assertTrue(defender.is_attackable(attacker))

    def test_defender_extinct(self):

        defender = Species(population=0)
        attacker = Species(traits=[Trait.CARNIVORE])

        self.assertFalse(defender.is_attackable(attacker))

    def test_attacker_neighbors(self):
        # Warning Call

        defender = Species(body=1)
        attacker = Species(traits=[Trait.CARNIVORE], body=2)
        neighbor = Species(traits=[Trait.WARNING_CALL])

        self.assertTrue(defender.is_attackable(attacker))
        self.assertFalse(defender.is_attackable(attacker, left=neighbor))
        self.assertFalse(defender.is_attackable(attacker, right=neighbor))

        attacker.traits = [Trait.CARNIVORE, Trait.AMBUSH]

        self.assertTrue(defender.is_attackable(attacker))
        self.assertTrue(defender.is_attackable(attacker, left=neighbor))
        self.assertTrue(defender.is_attackable(attacker, right=neighbor))

        # Symbiosis
        bigger_neighbor = Species(body=5)
        smaller_neighbor = Species(body=0)

        defender.traits = [Trait.SYMBIOSIS]

        self.assertTrue(defender.is_attackable(attacker))
        self.assertTrue(defender.is_attackable(attacker, left=bigger_neighbor))
        self.assertTrue(defender.is_attackable(attacker, right=smaller_neighbor))
        self.assertFalse(defender.is_attackable(attacker, right=bigger_neighbor))

    def test_defender_traits(self):
        # Burrowing
        defender = Species(food=0, population=1, traits=[Trait.BURROWING])
        attacker = Species(traits=[Trait.CARNIVORE])

        self.assertTrue(defender.is_attackable(attacker))

        defender.food = 1

        self.assertFalse(defender.is_attackable(attacker))

        # Climbing
        defender = Species(traits=[Trait.CLIMBING])
        attacker = Species(traits=[Trait.CARNIVORE])

        self.assertFalse(defender.is_attackable(attacker))

        attacker.traits = [Trait.CARNIVORE, Trait.CLIMBING]

        self.assertTrue(defender.is_attackable(attacker))

        # Hard Shell
        defender = Species(body=1, traits=[Trait.HARD_SHELL])
        attacker = Species(body=1, traits=[Trait.CARNIVORE])

        self.assertFalse(defender.is_attackable(attacker))

        attacker.body += HARD_SHELL_THRESHOLD

        self.assertTrue(defender.is_attackable(attacker))

        # Herding
        defender = Species(population=1, traits=[Trait.HERDING])
        attacker = Species(population=1, traits=[Trait.CARNIVORE])

        self.assertFalse(defender.is_attackable(attacker))

        attacker.population += 1

        self.assertTrue(defender.is_attackable(attacker))


class SituationTestCase(TestCase):

    NO_NEIGHBOR = False

    @staticmethod
    def attackable_from_situation(situation):
        """ Determines whether the second Species in the in the given Situation
        can attack the first, given the left and right neighbors of the defender.
        :param situation: JSON Situation
        :return: result of the situation
        """
        defender_data, attacker_data, left_data, right_data = situation

        defender = Species.from_json(defender_data)
        attacker = Species.from_json(attacker_data)
        left = Species.from_json(left_data) if left_data else None
        right = Species.from_json(right_data) if right_data else None

        return defender.is_attackable(attacker, left, right)

    @mock.patch.object(Species, "is_attackable")
    def test_attackable_from_situation(self, species_is_attackable):

        situations = [
            [Species().to_json(), Species().to_json(), self.NO_NEIGHBOR, self.NO_NEIGHBOR],
            [Species().to_json(), Species().to_json(), Species().to_json(), self.NO_NEIGHBOR],
            [Species().to_json(), Species().to_json(), self.NO_NEIGHBOR, Species().to_json()],
            [Species().to_json(), Species().to_json(), Species().to_json(), Species().to_json()],
        ]

        for situation in situations:

            attacker, defender, left, right = situation

            self.attackable_from_situation(situation)
            self.assertTrue(species_is_attackable.called)

            call_args = species_is_attackable.call_args[0]

            self.assertEqual(call_args[0].to_json(), attacker)

            if call_args[1] is None:
                self.assertEqual(left, self.NO_NEIGHBOR)
            else:
                self.assertEqual(call_args[1].to_json(), left)

            if call_args[2] is None:
                self.assertEqual(right, self.NO_NEIGHBOR)
            else:
                self.assertEqual(call_args[2].to_json(), right)
