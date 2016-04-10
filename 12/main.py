import sys
import json

from evolution.dealer import Dealer
from evolution.player import *

players_arg = sys.argv[1]
external_players = []

for x in range(1, int(players_arg) + 1):
    external_players.append(ExternalPlayer(x))

dealer = Dealer()
dealer.play_game(external_players)

scores = dealer.get_scores()

for x, player_score in enumerate(scores):
    out_string = str(x+1) + " player id: " + str(scores[x][1]) + " score: " + str(scores[x][0])
    sys.stdout.write(out_string + "\n")
