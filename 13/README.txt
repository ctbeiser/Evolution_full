Purpose: Implements the entirety of the game.

evolution/dealer.py
	Contains a representation of the Dealer in the game
evolution/traitcard.py
	Contains a representation of Trait Cards in the game
evolution/feeding_intent.py
	Contains all possible feeding intents returnable by Player
evolution/gui.py
	Contains a script that produces GUIs from dealers and players.
evolution/player.py
	Contains a representation of Player in the game
evolution/species.py
	Contains a representation of Species boards in the game
evolution/trait.py
	Contains a representation of Traits in the game
evolution/action.py
	Contains the representations of all possible player actions with Trait Cards
evolution/action4.py
	Contains the representation of all requested player actions for a turn
evolution/server.py
    Outer server for evolution game
evolution/proxy_dealer.py
    Wrapper for client for evolution game
evolution/validate.py
    Validation utilities
evolution/timeout.py
    Timing utility decorator

main
    Run the game with four players.
players.py
    Start a single player on port 45678
main.py
    Start a server on port 45678

compile
	Exits with code 0

Code can be read by beginning with the main. Continue to players.py and main.py.