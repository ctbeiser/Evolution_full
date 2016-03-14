import sys
import json

from dealer.dealer import Dealer

data = sys.stdin.read()
configuration = json.loads(data)
# The Configuration is [LOP+, Natural, LOC].

print(Dealer.deserialize(configuration).feed_one().serialize())