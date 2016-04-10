from .trait import Trait
from functools import total_ordering

# Because range is inclusive only on the bottom
CARNIVORE_FOOD_VALUE_RANGE = range(-8, 8+1)
NORMAL_FOOD_VALUE_RANGE = range(-3, 3+1)


@total_ordering
class TraitCard:
    def __init__(self, food_value, trait):
        """ Represents a Card with a Trait and a quantity of Food
        :param food_value: An Integer between -8 and 8
        :param trait: A Trait
        """
        if food_value in NORMAL_FOOD_VALUE_RANGE or \
                ((food_value in CARNIVORE_FOOD_VALUE_RANGE) and trait == Trait.CARNIVORE):
            self.food_value = food_value
        else:
            raise ValueError("Food value for a trait card must be in the acceptable range")
        self.trait = trait

    def __lt__(self, other):
        if self.trait < other.trait:
            return True
        elif self.trait == other.trait:
            return self.food_value < other.food_value
        else:
            return False

    def __eq__(self, other):
        return self.trait == other.trait and self.food_value == other.food_value


    def make_tree(self, tree, parent):
        """ Modify the ttk tree provided to add a representation of this data structure
        :param tree: a ttk Treeview widget object
        :param parent: the ttk reference to a row in the ttk Treeview under which this content should be added.
        """
        tree.insert(parent, 'end', text=(str(self.food_value) + ", " + self.trait.serialize()))

    def serialize(self):
        """ Returns a serialized version of the Card
        :return: serialized version of the Card
        """
        return [self.food_value, self.trait.serialize()]

    @classmethod
    def deserialize(cls, data):
        """ Given a serialized Card,
        :param data: A list of [foodValue, name] where the former is between
        -8 and 8, and the latter is a serialized trait
        :return: a new TraitCard
        """
        food_value, name = data
        return cls(food_value, Trait(name))

    @staticmethod
    def new_deck():
        """ Generate a new unshuffled Deck according to the rules of Evolution
        :return: a List of TraitCard
        """
        deck = []
        for t in Trait:
            food_range = NORMAL_FOOD_VALUE_RANGE
            if t == Trait.CARNIVORE:
                food_range = CARNIVORE_FOOD_VALUE_RANGE
            for i in range(food_range):
                deck.append(TraitCard(i, t))
        assert(len(deck) == 122)
        return deck
