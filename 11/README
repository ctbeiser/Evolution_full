Purpose: Implement the step4 method, a test harness for said method, and specify the protocol for a future main method that interacts with an external player
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
api/Ending_a_Game.png
	An interaction diagram for ending a game of Evolution
api/Per_Turn.png
	An interaction diagram for a single turn of Evolution
api/Starting_a_Game.png
	An interaction diagram for starting a game of Evolution
api/Interaction Protocol.txt
	Notes that include protocol details not captured in interaction diagrams
Tests:
evolution/test_feeding_intent.py
	Tests for feeding_intent.py
evolution/test_player.py
	Tests for player.py
evolution/test_species.py
	Tests for species.py
evolution/test_dealer.py
	Tests for dealer.py


test/*
	JSON Test files for project test harness. Input files are denoted as X-in.json, output files as X-out.json

xstep4.py
	A test harness for testing 'step4' method in Dealer. Accepts input from stdin and outputs to stdout

xstep4
	A bash script that calls xstep4.py
compile
	Exits with code 0

Code can be read by beginning with the action.py file. Continue to the action4.py file. From there read over the step4 method in Dealer.py

The tests can be run with the following command:
    python3 -m unittest

 The xstep4 tests can be run from the assignment root with:
    for i in {1..5}; do ./xstep4 < test/$i-in.json | cmp test/$i-out.json; done