This assignment implements a game representation for Player and an executable
 to determine the outcome of a call by the dealer on the Player to choose the
 next species to feed.

feeding/player.py
 contains a representation of Player in the game

feeding/feeding_intent.py
 contains all possible feeding intents returnable from xfeed

feeding/species.py
 contains the implementation of Species

feeding/trait.py
 contains the implementation of Trait

feeding/test_player.py
 tests for player.py

feeding/test_species.py
 tests for species.py

compile
 exits with code 0

xfeed
 wrapper to call xfeed.py

xfeed.py
 reads a feeding situation JSON from stdin and outputs a feeding intent
 to stdout based on the Player's feeding strategy

test/*
 test files for xfeed, X-in.json contains the feeding situation and X-out.json
 contains the desired output of xfeed

The code should be read starting with xfeed.py which uses the Player's
 deserialize method to create Player objects from the given feeding
 situation JSON. With these objects the scripts calls the Player's
 method next_species_to_feed, which then handles the individual feeding
 cases (store fat, feed vegetarian, feed carnivore and no species to feed).

 The tests can be run with the following command:
    python3 -m unittest

 The xfeed tests can be run from the assignment root with:
    for i in {1..5}; do ./xfeed < test/$i-in.json | cmp test/$i-out.json; done