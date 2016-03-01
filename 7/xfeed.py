import sys
import json

from feeding.player import Player

data = sys.stdin.read()
feeding = json.loads(data)

# A Feeding is [Player, Natural+, LOP]. The natural number in the middle
# specifies how many tokens of food are left at the watering hole.

player_data, watering_hole_data, other_players_data = feeding

player = Player.deserialize(player_data)
other_players = [Player.deserialize(p) for p in other_players_data]

resolution = player.next_species_to_feed(other_players, watering_hole_data)

# CannotFeed raises a value error
try:
    print(json.dumps(resolution.serialize()))
except ValueError:
    pass

