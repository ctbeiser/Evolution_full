import sys
import json

from evolution.dealer import Dealer, MIN_PLAYERS
from evolution.player import *
from evolution.server import Server

server = Server("localhost", 45678)
remote_players = server.add_players()

dealer = Dealer()
proxies = [ProxyPlayer(p) for p in remote_players]
dealer.play_game(proxies)

scores = dealer.get_scores()

for x, player_score in enumerate(scores):
    out_string = str(x+1) + " player id: " + str(scores[x][1]) + " score: " + str(scores[x][0])
    sys.stdout.write(out_string + "\n")
