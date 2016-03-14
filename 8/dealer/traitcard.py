from feeding.trait import Trait

# Because range is inclusive only on the bottom
FOOD_VALUE_RANGE = range(-8, 8+1)


class TraitCard:
    def __init__(self, food_value, trait):
        """
        :param food_value: An Integer between -8 and 8
        :param trait: A Trait
        :return:
        """
        if food_value in FOOD_VALUE_RANGE:
            self.food_value = food_value
        else:
            raise ValueError("Food value for a trait card must be in the acceptable range")
        self.trait = trait

    def serialize(self):
        """ Returns a serialized version of the Card
        :return: serialized version of the Card
        """
        return [self.food_value, self.trait.serialize()]

    @classmethod
    def deserialize(cls, data):
        """ Given a serialized Card,
        :param data: A list of [foodValue, name] where the former is
        :return:
        """
        food_value, name = data
        return cls(food_value, Trait(name))