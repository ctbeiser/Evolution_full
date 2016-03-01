"""

Represents a Species in the Evolution game.

"""

from .trait import Trait, HARD_SHELL_THRESHOLD


SPECIES_DEFAULT_FOOD = 0
SPECIES_DEFAULT_BODY = 0
SPECIES_DEFAULT_POPULATION = 1


class Species:

    def __init__(self,
                 food=SPECIES_DEFAULT_FOOD,
                 body=SPECIES_DEFAULT_BODY,
                 population=SPECIES_DEFAULT_POPULATION,
                 traits=None):
        """ Creates a new Species
        :param food: number food tokens the species has
        :param body: body size of the species
        :param population: population size of the species
        :param traits: list of traits
        """
        self.food = food
        self.body = body
        self.population = population
        self.traits = traits or []

    @classmethod
    def from_json(cls, data):
        """ Creates a new Species object from a JSON representation of a
        Species. The JSON representation has the following format:
           [ ["food",Nat],
             ["body",Nat],
             ["population",Nat],
             ["traits",LOT] ]
        where LOT is a list of trait strings.
        :param data: JSON representation of a Species
        :return: Species object
        """
        parameters = {parameter: value for parameter, value in data}
        trait_list = parameters.pop("traits", [])
        traits = [Trait(trait) for trait in trait_list]

        return cls(food=parameters.get('food'),
                   body=parameters.get('body'),
                   population=parameters.get('population'),
                   traits=traits)

    def to_json(self):
        """ Generates a JSON representation of the Species
        :return: JSON representation of the Species
        """
        return [
            ["food", self.food],
            ["body", self.body],
            ["population", self.population],
            ["traits", [trait.value for trait in self.traits]],
        ]

    def has_trait(self, trait):
        """ Check whether this Species has the given Trait
        :param trait: Trait to check the presence of
        :return: true if this Species has the given Trait, else false
        """
        return trait in self.traits

    def is_attackable(self, attacker, left=None, right=None):
        """ Determines whether this species is attackable by the given species,
        given this species left and right neighbor.
        :param attacker: Species that is attacking
        :param left: Species on the left of this Species or None
        :param right: Species on the right of this Species or None
        :return: true if this species is attackable, else false
        """
        attacker_body = attacker.body + (4 if attacker.has_trait(Trait.PACK_HUNTING) else 0)

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
            (self.has_trait(Trait.HARD_SHELL) and (attacker_body - self.body) < HARD_SHELL_THRESHOLD),
            (self.has_trait(Trait.HERDING) and attacker.population <= self.population),
            (self.has_trait(Trait.SYMBIOSIS) and right and right.body > self.body),
        ]

        return not any(failure_reasons)