"""

A Card is a namedtuple of (value, bullvalue), where value is a Value, and
    bullvalue is a BullValue
A Value is an Integer in the range [1, 104]
A BullValue is an Integer in the range [2, 7]
A Stacks is a 4-tuple of list of Card, with the bottom of the stack first
a Deck is a list of Card, with the topmost card at the end

"""

from collections import namedtuple


Card = namedtuple("Card", "value bullvalue")


def default_number_bullpoint_mapping(card_value):
    """ Returns a BullValue based on 6Nimmt! rules for the given card value.
    :param card_value: card value for which to return BullValue
    :return: bull points assigned to the given card value
    """
    # 1 card with 7 cattle heads—number 55
    if card_value == 55:
        return 7
    # 8 cards with 5 cattle heads—the multiples of 11, i.e. 11, 22, 33,
    elif card_value % 11 == 0:
        return 5
    # 10 cards with 3 cattle heads—the multiples of ten, i.e. 10, 20, 30,
    elif card_value % 10 == 0:
        return 3
    # 9 cards with 2 cattle heads—the multiples of five which are not
    elif card_value % 5 == 0:
        return 2
    # 76 cards with 1 cattle head—the rest of the cards from 1 through 104
    else:
        return 1


def create_deck(number_bullpoint_mapping=default_number_bullpoint_mapping):
    """ Creates a new Deck of cards according to the 6Nimmt rules
    :param number_bullpoint_mapping: a function that returns the desired number of bullpoints
                                     for each given card value, the returned number must be a BullValue
    :return: a Deck of cards
    """
    return [Card(n, number_bullpoint_mapping(n)) for n in range(1, 105)]
