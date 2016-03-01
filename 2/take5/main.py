"""

Simulates a game of 6Nimmt! with the specified number of players.
At the end of the game the bull points of all players are printed out with
the player numbers, sorted from the least amount of bull points.

Usage: python main.py

"""

from dealer import Dealer
from dummy_player import DummyPlayer


def simulate_game(num_players):
    """ Simulate a game of 6Nimmt! for the given number of players.
    :param num_players: number of players in the simulation
    :return: an integer if an error occurred, otherwise None
    """
    players = [DummyPlayer(i, num_players) for i in range(num_players)]
    dealer = Dealer(players)
    dealer.game()
    return dealer.stats()


def main():
    """ Asks the user to choose the number of players and starts a simulation of the game.
    :return: an integer if an error occurred, otherwise None
    """
    try:
        num_players = int(input("Enter the number of players: "))
    except ValueError:
        print("Invalid number entered.")
        return 1

    if num_players > 10:
        print("A maximum of 10 players is supported.")
        return 1

    game_stats = simulate_game(num_players)

    for player_id, bull_points in game_stats:
        print("Player {}: {} bull points".format(player_id, bull_points))

if __name__ == "__main__":
    main()
