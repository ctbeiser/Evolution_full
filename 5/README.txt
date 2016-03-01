This project includes a JSON species attack tester, and a dealer interface.

FILES
Attack/
  __init__.py : Necessary for Python to recognize this folder as a module
  species.py : Represents a Species in the Evolution game
  test_species.py : Tests species.py
  trait.py : Represents a Trait in the Evolution game
player-interface.txt : Specifies a player for the Evolution game
xattack : Runs a test of whether a given attack, as JSON can be executed.
xattack_tests : A set of sample inputs to be piped into x-attack.
  1-in.json : A test that should return the result in 1-out.json
  2-in.json : A test that should return the result in 2-out.json
  1-out.json : Results for 1-in.json
  2-out.json : Results for 2-in.json
  
The code may be run by running `./xattack' in this directory.

To understand the code, start by reading trait.py, and then read species.py, and 
xattack.
