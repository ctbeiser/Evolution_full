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

for x in range(1, int(players_arg) + 1):
    out_string = str(x)
    sys.stdout.write(out_string + dealer.get_score(x) + "\n")
