This folder contains an implementation of "6Nimmt!".

player.py -- An implementation of the Player interface that was provided.
player_tests.py -- Tests for the Player interface that was provided.
take5/main.py -- The main program to run the game.
take5/dealer.py -- A Dealer implementation which controls game flow and state.
take5/player.py -- A Player implementation which pursues a basic strategy.

take5/tests -- Home of all the tests for our take5 implementation.
take5/tests/test_dealer.py -- Tests for the Dealer implementation.
take5/tests/test_place_cards_state.py -- Tests for correctly placing the given card in a stack.
take5/tests/test_main.py -- Tests for starting our take5 game.
take5/tests/test_run_game.py -- Tests for ensuring proper game state transitions.

In order to launch the game, run `python3 main.py [number of players]`.
This runs the game and will print out the index numbers and bull points of players,
sorted in increasing order at the end of the game.

In order to understand the program, the best place to start is by looking
through the take5/dealer.py. This contains the Dealer component which is
responsible for managing the rules and state of the game. Start with the
run_game() method in the dealer.py and follow the code from there.
