import sys
import json

from evolution.player import *

data = sys.stdin.read()
input_array = json.loads(data)

player_data = input_array[0]
player = ExternalPlayer.deserialize(player_data)
before_los = input_array[1]
after_los = input_array[2]

sys.stdout.write(json.dumps(player.choose(before_los, after_los)))