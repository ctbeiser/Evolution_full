This project implements the provided player interface and
 the Dealer and main components of our specification.


player.txt: a memo explaining the impossibility of implementing
 the given player specification
take5/main.py: runs a 6Nimmt! simulation
take5/dealer.py: the implementation of the Dealer component
take5/definitions.py: key definitions required for the program
take5/player_state.py: adds hand and point tracking to Player
take5/dummy_player.py: simple implementation of Player for testing
take5/test_{name}.py: tests for the {name}.py file


The game can be run from the take5 directory by typing:
    `python3 main.py`


The program should be read starting with definitions.py for the
 reader to become familiarized with the definitions used
 throughout the code. The reader should continue with the
 player_state.py to understand the additional functionality
 that is added to each Player. The next file to read should be
 dealer.py, which brings the definitions and the player states
 together to simulate a game. Finally, main.py shows how
 a dealer is instantiated and how a game is simulated.