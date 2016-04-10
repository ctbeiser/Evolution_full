import sys
import json

from evolution.player import *

players_arg = sys.argv[1]
external_players = []

for x in range(1, players_arg + 1):
	external_players.append(ExternalPlayer(x))

dealer = Dealer(0)
dealer.play_game(external_players)

for x in range(1, players_arg + 1):
	out_string = ""
	out_string += x
	sys.stdout.write(out_string.append(dealer.get_score(x)))
