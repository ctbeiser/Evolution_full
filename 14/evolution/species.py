"""

Represents a Species in the Evolution game.

"""
from .trait import Trait, HARD_SHELL_THRESHOLD
from .validate import *

SPECIES_DEFAULT_FOOD = 0
SPECIES_DEFAULT_BODY = 0
SPECIES_DEFAULT_POPULATION = 1
SPECIES_MAX_POPULATION = 7
SPECIES_DEFAULT_FAT_FOOD = 0
FOOD_NAME = 'food'
BODY_NAME = 'body'
POPULATION_NAME = 'population'
TRAITS_NAME = 'traits'
FAT_FOOD_NAME = 'fat-food'
MAX_TRAITS = 3


class Species:
    def __init__(self,
                 food=SPECIES_DEFAULT_FOOD,
                 body=SPECIES_DEFAULT_BODY,
                 population=SPECIES_DEFAULT_POPULATION,
                 traits=None,
                 fat_food=None):
        """ Creates a new Species
        :param food: number food tokens the species has
        :param body: body size of the species
        :param population: population size of the species
        :param traits: list of traits
        :param fat_food: food tokens stored on fat tissue traits, must be 0 if
                         the species doesn't have any fat tissue traits
        """
        self.food = food
        self.body = body
        self._population = population
        self.traits = traits or []
        self.verify_traits()
        self.fat_food = fat_food or SPECIES_DEFAULT_FAT_FOOD

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        value = min(value, SPECIES_MAX_POPULATION)
        # TODO :  Add killing the creature to here... somehow.
        self._population = value
        self.food = min(self.food, self._population)

    def replace_trait_at_index(self, idx, trait):
        self.traits[idx] = trait
        self.verify_traits()

    def verify_traits(self):
        if not self.has_trait(Trait.FAT_TISSUE):
            self.fat_food = 0
        if not all([(not(any(self.traits.count(x) > 1 for x in self.traits))),
                   len(self.traits) <= MAX_TRAITS]):
            raise ValueError()

    @classmethod
    def deserialize(cls, data):
        """ Creates a new Species object from a Species+

           [ ["food",Nat],
             ["body",Nat],
             ["population",Nat],
             ["traits",LOT] ]

            or

           [ ["food",Nat],
             ["body",Nat],
             ["population",Nat+],
             ["traits",LOT],
             ["fat-food", Nat] ]

        where LOT is a list of trait strings.

        :param data: a Species+ as JSON
        :return: Species object
        This method will raise a ValueError given a bad Species
        """
        # Ensure the items are in order:
        if not all([is_list(data),
                    4 <= len(data) <= 5,
                    all([is_list(i) for i in data]),
                    all([(len(i) == 2) for i in data]),
                    data[0][0] == FOOD_NAME,
                    data[1][0] == BODY_NAME,
                    data[2][0] == POPULATION_NAME,
                    data[3][0] == TRAITS_NAME]):
            raise ValueError()

        parameters = {parameter: value for parameter, value in data}
        trait_list = parameters.pop(TRAITS_NAME, [])
        traits = [Trait(trait) for trait in trait_list]

        return cls(food=parameters.get(FOOD_NAME),
                   body=parameters.get(BODY_NAME),
                   population=parameters.get(POPULATION_NAME),
                   traits=traits,
                   fat_food=parameters.get(FAT_FOOD_NAME))

    def serialize(self):
        """ Generates a data representation of Species
        :return: data representation of the Species
        """
        data = [
            [FOOD_NAME, self.food],
            [BODY_NAME, self.body],
            [POPULATION_NAME, self.population],
            [TRAITS_NAME, [trait.value for trait in self.traits]],
        ]

        if self.has_trait(Trait.FAT_TISSUE) and self.fat_food:
            data.append([FAT_FOOD_NAME, self.fat_food])

        return data

    def has_trait(self, trait):
        """ Check whether this Species has the given Trait
        :param trait: Trait to check the presence of
        :return: true if this Species has the given Trait, else false
        """
        return trait in self.traits

    @property
    def attacking_body(self):
        """ The body size of the species if it is attacking.
        :return: body size of this species if it acts as an attacker
        """
        return self.body + (self.population if self.has_trait(Trait.PACK_HUNTING) else 0)

    def is_attackable(self, attacker, left=None, right=None):
        """ Determines whether this species is attackable by the given species,
        given this species left and right neighbor.
        :param attacker: Species that is attacking
        :param left: Species on the left of this Species or None
        :param right: Species on the right of this Species or None
        :return: true if this species is attackable, else false
        """
        failure_reasons = [
            # defender must have at least one population
            (self.population == 0),
            # can only be attacked by a carnivore
            (not attacker.has_trait(Trait.CARNIVORE)),
            # neighbors can have Warning Call
            ((left and left.has_trait(Trait.WARNING_CALL) or
              right and right.has_trait(Trait.WARNING_CALL)) and
                not attacker.has_trait(Trait.AMBUSH)),
            # individual traits
            (self.has_trait(Trait.BURROWING) and self.food == self.population),
            (self.has_trait(Trait.CLIMBING) and not attacker.has_trait(Trait.CLIMBING)),
            (self.has_trait(Trait.HARD_SHELL) and (attacker.attacking_body - self.body) < HARD_SHELL_THRESHOLD),
            (self.has_trait(Trait.HERDING) and attacker.population <= self.population),
            (self.has_trait(Trait.SYMBIOSIS) and right and right.body > self.body),
        ]

        return not any(failure_reasons)

    def is_hungry(self):
        """ Returns true if this species is not fully fed.
        :return: true if the this species is hungry
        """
        return self.food < self.population

    def trait_count(self):
        return len(self.traits)