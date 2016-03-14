import sys
import json

from dealer.dealer import Dealer

data = sys.stdin.read()
configuration = json.loads(data)
# The Configuration is [LOP+, Natural, LOC].

print(configuration)

dealer = Dealer.deserialize(configuration)
dealer.feed_one(dealer.players)

print(dealer.serialize())