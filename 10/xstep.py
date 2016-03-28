import sys
import json

from evolution import Dealer

data = sys.stdin.read()
configuration = json.loads(data)
# The Configuration is [LOP+, Natural, LOC].

dealer = Dealer.deserialize(configuration)
dealer.feed_one(dealer.players)

sys.stdout.write(json.dumps(dealer.serialize()))