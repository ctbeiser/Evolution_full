This assignment implements an echo program that accepts JSON data from stdin
 and writes valid JSON back to stdout. It also includes the xfeed script with
 the requested API changes.


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

xattack
 wrapper to call xattack.py

xfeed.py
 runs a test of whether a given attack, as JSON can be executed

test/*
 test files for xfeed, X-in.json contains the feeding situation and X-out.json
 contains the desired output of xfeed

Streaming/compile
 exits with code 0

Streaming/xstream
 wrapper to call xstream.py

Streaming/xstream.py
 accepts input from stdin, parses valid JSON values and prints them back to
 stdout

Streaming/test/*
 test files for xstream, X-in.json contains the feeding situation and X-out.json
 contains the desired output of xstream



The code should be read starting with xfeed.py which uses the Player's
 deserialize method to create Player objects from the given feeding
 situation JSON. With these objects the scripts calls the Player's
 method next_species_to_feed, which then handles the individual feeding
 cases (store fat, feed vegetarian, feed carnivore and no species to feed).

 The tests can be run with the following command:
    python3 -m unittest

 The xfeed tests can be run from the assignment root with:
    for i in {1..5}; do ./xfeed < test/$i-in.json | cmp test/$i-out.json; done

 The xstream tests can be run from Streaming with:
    for i in {1..5}; do ./xstream < test/$i-in.json | cmp test/$i-out.json; done
