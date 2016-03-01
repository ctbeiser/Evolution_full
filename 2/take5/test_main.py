from unittest import TestCase
from unittest.mock import patch

from main import simulate_game


class MainTests(TestCase):

    @patch("main.Dealer")
    def test_simulate_game(self, mock_dealer):

        simulate_game(10)
        self.assertEqual(len(mock_dealer.call_args[0][0]), 10)
        mock_dealer.return_value.game.assert_called_once_with()
        mock_dealer.return_value.stats.assert_called_once_with()

