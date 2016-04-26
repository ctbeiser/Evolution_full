import sys

from evolution.dealer import Dealer, MIN_PLAYERS
from evolution.player import ExternalPlayer
from evolution.server import Server
from evolution.debug import debug
from evolution.proxy_player import ProxyPlayer

def generate_score_string(scores):
    """ Print out the scores for the end of the game
    :param scores: a List(Integer, Integer, String), representing score, player ID, and Handshake respectively
    :return String describing the score
    """
    result = ""
    for x, player_score in enumerate(scores):
        out_string = str(x+1) + " player id: " + str(player_score[1]) + \
                     " score: " + str(player_score[0]) + \
                     " handshake: " + player_score[2] + "\n"
        result += out_string
    return result

def main(port):
    """ Carry out the game and print results to stdout
    :param port: Integer representing the port to play on
    """
    if port:
        server = Server("localhost", port)
        remote_players_and_messages = server.add_players()
        proxies = [(ProxyPlayer(p[0]), p[1]) for p in remote_players_and_messages]
    else:
        proxies = [(ExternalPlayer(i), "hi") for i in range(5)]

    dealer = Dealer()
    dealer.play_game(proxies)

    scores = dealer.get_scores()
    if not scores:
        debug("Every player dropped and the game ended")
    sys.stdout.write(generate_score_string(scores))

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = None
    main(port)