import unittest
import unittest.mock

from remote_player import RemotePlayer, Card, MessageTypes, ResponseErrors


class RemotePlayerTestCase(unittest.TestCase):

    def setUp(self):

        with unittest.mock.patch("remote_player.StreamingJSONCoder", new=unittest.mock.MagicMock):
            self.remote_player = RemotePlayer("localhost", 45678)

    def test_encode_decode_card(self):

        test_card_json = [1, 2]
        test_card_game = Card(1, 2)

        self.assertEqual(RemotePlayer.decode_card(test_card_json), test_card_game)
        self.assertEqual(RemotePlayer.encode_card(test_card_game), test_card_json)
        self.assertEqual(RemotePlayer.decode_card(RemotePlayer.encode_card(test_card_game)), test_card_game)
        self.assertEqual(RemotePlayer.encode_card(RemotePlayer.decode_card(test_card_json)), test_card_json)

    def test_encode_decode_stacks(self):

        # test empty
        test_stacks_empty_json = []
        test_stacks_empty_game = ()

        self.assertEqual(RemotePlayer.decode_stacks(test_stacks_empty_json), test_stacks_empty_game)

        # test with data

        test_stacks_json = [
            [[1, 2], [4, 5]],
            [[3, 4]],
            [[1, 2]],
        ]
        test_stacks_game = (
            [Card(1, 2), Card(4, 5)],
            [Card(3, 4)],
            [Card(1, 2)],
        )

        self.assertEqual(RemotePlayer.decode_stacks(test_stacks_json), test_stacks_game)

    def test_process_message_invalid(self):
        """ Return false on invalid messages
        """
        invalid_messages = [
            {},
            False,
            "truth",
            {"some": "object"},
            ["one"],
            5,
        ]

        for message in invalid_messages:
            self.assertEqual(self.remote_player.process_message(message),
                             ResponseErrors.INVALID_MESSAGE)

        unknown_messages = [
            ["some", "message"],
            ["another", "message"],
        ]

        for message in unknown_messages:
            self.assertEqual(self.remote_player.process_message(message),
                             ResponseErrors.INVALID_MESSAGE)

    def test_process_message_valid(self):
        """ Check that the correct methods were called
        """
        # replace message type to method mapping
        for message_type in MessageTypes:
            self.remote_player.MESSAGE_METHOD_MAPPING[message_type] = unittest.mock.MagicMock()

        messages = [[message_type.value, "argument"] for message_type in MessageTypes]

        # check that the correct methods get called
        for message in messages:
            self.remote_player.process_message(message)

            message_type = MessageTypes(message[0])
            message_argument = message[1]
            self.remote_player.MESSAGE_METHOD_MAPPING[message_type].assert_called_once_with(message_argument)
            self.assertEqual(self.remote_player.last_message, message_type)

    def test_start_round_invalid_data(self):
        # player must not have any cards, otherwise there will be a timing violation
        self.remote_player.hand = []

        arguments = [
            1,
            [],
            [123],
            [Card(1, 2)],
            {}
        ]

        for argument in arguments:
            self.assertEqual(self.remote_player.start_round(argument), ResponseErrors.INVALID_MESSAGE)

    def test_start_round_timing_violation(self):

        self.remote_player.hand = [Card(1, 2)]

        self.assertEqual(self.remote_player.start_round([[1, 2]]), ResponseErrors.TIMING_VIOLATION)

        # but if there is a timing violation, invalid message should have a higher priority
        arguments = [
            1,
            [],
            [123],
            [Card(1, 2)],
            {}
        ]

        for argument in arguments:
            self.assertEqual(self.remote_player.start_round(argument), ResponseErrors.INVALID_MESSAGE)

    def test_take_turn_invalid_data(self):
        # player must have at least one card
        self.remote_player.hand = [Card(1, 1)]

        arguments = [
            1,
            [123],
            [Card(1, 2)],
            {}
        ]

        for argument in arguments:
            self.assertEqual(self.remote_player.take_turn(argument), ResponseErrors.INVALID_MESSAGE)

    def test_take_turn_timing_violation(self):

        self.remote_player.hand = []

        self.assertEqual(self.remote_player.take_turn([]), ResponseErrors.TIMING_VIOLATION)

        # but if there is a timing violation, invalid message should have a higher priority
        arguments = [
            1,
            [123],
            [Card(1, 2)],
            {}
        ]

        for argument in arguments:
            self.assertEqual(self.remote_player.take_turn(argument), ResponseErrors.INVALID_MESSAGE)

    def test_choose_invalid_data(self):
        # last message must be take turn
        self.remote_player.last_message = MessageTypes.TAKE_TURN

        arguments = [
            1,
            [123],
            [Card(1, 2)],
            {}
        ]

        for argument in arguments:
            self.assertEqual(self.remote_player.choose(argument), ResponseErrors.INVALID_MESSAGE)

    def test_choose_timing_violation(self):

        self.remote_player.last_message = MessageTypes.START_ROUND

        self.assertEqual(self.remote_player.choose([[[1, 2]]]), ResponseErrors.TIMING_VIOLATION)

        # but if there is a timing violation, invalid message should have a higher priority
        arguments = [
            1,
            [123],
            [Card(1, 2)],
            {}
        ]

        for argument in arguments:
            self.assertEqual(self.remote_player.choose(argument), ResponseErrors.INVALID_MESSAGE)


