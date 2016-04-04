import sys
import json

from evolution.dealer import Dealer
from evolution.action4 import Action4

data = sys.stdin.read()
input_array = json.loads(data)

configuration = input_array[0]
step_four = input_array[1]

# The Configuration is [LOP+, Natural, LOC].
dealer = Dealer.deserialize(configuration)
action_fours = [Action4.deserialize(step) for step in step_four]

dealer.step_four(action_fours)

sys.stdout.write(json.dumps(dealer.serialize()))