"""

This file implements a remote Player based on the communication protocol
that acts as a proxy between the server and the Player from assignment 3.


JSON Data Definitions:

A Name is a JSON string.

A Integer is a JSON number interpretable as a positive integer.

A Card is [Integer, Integer].
constraint: the first Integer is face value, as described by the requirements analysis for 6 Nimmt!
constraint: the second Integer are bull points, as described by the requirements analysis for 6 Nimmt!

A LCard is [Card, ..., Card].

A Stack is an LCard that contains at least one Card.

A Deck is [Stack, ..., Stack].

"""

import os
import sys

from collections import namedtuple
from enum import Enum

from streaming_json_coder import StreamingJSONCoder

PATH_TO_PLAYER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "3", "take5")
sys.path.insert(0, PATH_TO_PLAYER)

# player from assignment 3
from player import Player

Card = namedtuple("Card", "value bullvalue")

PLAYER_INDEX_DEFAULT = 0
NUMBER_OF_PLAYERS_DEFAULT = 0
TIMING_VIOLATION_RESPONSE = False


class MessageTypes(Enum):
    """ Represents the messages that the player can process.
    """
    START_ROUND = "start-round"
    TAKE_TURN = "take-turn"
    CHOOSE = "choose"


class ResponseErrors(Enum):
    """ Represents error that can occur when processing messages.
    """
    INVALID_MESSAGE = 0
    TIMING_VIOLATION = 1


class DataDefinitions:
    """ Implements the data definitions.
    """

    # ranges are [min, max)
    CARD_VALUE_RANGE = range(1, 105)
    CARD_BULL_RANGE = range(2, 8)

    @staticmethod
    def is_name(value):
        """ Determines whether the value is a Name
        :param value: Name candidate
        :return: True if the value is a Name
        """
        return isinstance(value, str)

    @staticmethod
    def is_integer(value):
        """ Determines whether the value is an Integer
        :param value: Integer candidate
        :return: True if the value is an Integer
        """
        return isinstance(value, int) and value > 0

    @classmethod
    def is_card(cls, value):
        """ Determines whether the value is a Card
        :param value: Card candidate
        :return: True if the value is a Card
        """
        return (isinstance(value, list) and len(value) == 2 and
                value[0] in cls.CARD_VALUE_RANGE and
                value[1] in cls.CARD_BULL_RANGE)

    @classmethod
    def is_lcard(cls, value):
        """ Determines whether the value is a LCard
        :param value: LCard candidate
        :return: True if the value is a LCard
        """
        return isinstance(value, list) and all(cls.is_card(x) for x in value)

    @classmethod
    def is_stack(cls, value):
        """ Determines whether the value is a Stack
        :param value: Stack candidate
        :return: True if the value is an Stack
        """
        return cls.is_lcard(value) and len(value) > 0

    @classmethod
    def is_deck(cls, value):
        """ Determines whether the value is a Deck
        :param value: Deck candidate
        :return: True if the value is a Deck
        """
        return isinstance(value, list) and all(cls.is_stack(x) for x in value)


class RemotePlayer:
    """ Listens for JSON messages on a url and port, if the messages are
    valid it processes them and calls the appropriate methods on Player.
    """

    def __init__(self, host, port):
        """
        :param host:
        :param port:
        :return:
        """
        self.host = host
        self.port = port

        self.coder = StreamingJSONCoder(self.host, self.port)

        # message to method mapping
        self.MESSAGE_METHOD_MAPPING = {
            MessageTypes.START_ROUND: self.start_round,
            MessageTypes.TAKE_TURN: self.take_turn,
            MessageTypes.CHOOSE: self.choose,
        }

        # variables need for the game
        self.player = Player(player_index=PLAYER_INDEX_DEFAULT,
                             number_of_players=NUMBER_OF_PLAYERS_DEFAULT)
        self.hand = None
        self.last_message = None

    def process_messages(self):
        """ Continuously processes messages until we run out.
        """
        for message in self.coder.decode():

            output = self.process_message(message)

            if output in ResponseErrors:
                if output == ResponseErrors.TIMING_VIOLATION:
                    self.coder.encode(TIMING_VIOLATION_RESPONSE)

                self.coder.shutdown()
                exit(1)

            # encode and send the output back
            self.coder.encode(output)

    def process_message(self, message):
        """ Process a JSON object that could a be a message
        :param message: JSON object
        :return: JSON data to send as a response
        """
        if not isinstance(message, list) or len(message) != 2:
            return ResponseErrors.INVALID_MESSAGE

        # a message consists of message_type, argument
        message_type_string, argument = message

        try:
            message_type = MessageTypes(message_type_string)
        except ValueError:
            return ResponseErrors.INVALID_MESSAGE

        response = self.MESSAGE_METHOD_MAPPING[message_type](argument)
        self.last_message = message_type
        return response

    def start_round(self, cards):
        """ Hands out cards to the player.
        :param cards: list of Card
        :return: False if the call violates timing constraints else True
        """
        # check that the data is of the correct type
        if not DataDefinitions.is_lcard(cards) or not cards:
            return ResponseErrors.INVALID_MESSAGE
        # if the player has cards in hand, this call is invalid
        elif self.hand:
            return ResponseErrors.TIMING_VIOLATION
        else:
            self.hand = [self.decode_card(card) for card in cards]
            return True

    def take_turn(self, deck):
        """
        :param deck: Deck representing the stacks in the game
        :return: False if the call violates timing constraints else the
                 chosen Card
        """
        # check that the data is of the correct type
        if not DataDefinitions.is_deck(deck):
            return ResponseErrors.INVALID_MESSAGE
        # if the hand is empty, this call is invalid
        if not self.hand:
            return ResponseErrors.TIMING_VIOLATION
        else:
            stacks = self.decode_stacks(deck)
            card = self.player.on_new_turn(self.hand, stacks)
            # remove the card from the hand
            self.hand.remove(card)
            return self.encode_card(card)

    def choose(self, deck):
        """
        :param deck: Deck representing the stacks in the game
        :return:
        """
        # check that the data is of the correct type
        if not DataDefinitions.is_deck(deck):
            return ResponseErrors.INVALID_MESSAGE
        # choose can only be called after take turn
        elif self.last_message != MessageTypes.TAKE_TURN:
            return ResponseErrors.TIMING_VIOLATION
        else:
            stacks = self.decode_stacks(deck)
            chosen_stack_index = self.player.choose_stack_to_take(stacks)
            return deck[chosen_stack_index]

    @staticmethod
    def decode_card(card):
        """ Converts a JSON Card to a take5 card.
        :param card: JSON card
        :return: take5 card
        """
        return Card(card[0], card[1])

    @staticmethod
    def encode_card(card):
        """ Converts a take5 card to a JSON Card
        :param card: take5 card
        :return: JSON Card
        """
        return [card.value, card.bullvalue]

    @classmethod
    def decode_stacks(cls, deck):
        """ Converts a Deck into take5 Stacks
        :param deck: Deck
        :return: take5 Stacks
        """
        return tuple([cls.decode_card(c) for c in stack] for stack in deck)

