This project implments a Player based on our specifications and the provided
 strategy. It also includes patches that implement the changes outlined in the
 assignment. The patches build on top of one another and therefore should be
 applied in sequence.


take5/patches/0001-replace-dummy-player-with-new-player-from-3.patch
These changes are necessary to link the player in its new location. This
 required adding additional code in to main.py in order to locate the player in
 the filesystem, as Python doesn't have the needed support of relative imports.

take5/patches/0002-make-stack-size-configurable-and-add-defaults.patch
For this part, we had to parametrize the maximum stack size so that it could
 be altered without breaking existing tests. We also had to fix tests that
 didn't account for the possibility of running the main game method with
 arguments.

take5/patches/0003-make-number-of-cards-configurable-and-add-default.patch
Though we supported multiple strategies for assigning bullpoints to a deck, we
 didn't have a way to change the length of the deck without breaking the
 existing tests. We have therefore parametrized create_deck to take an
 additional parameter for the size of the deck, modified the existing tests to
 explicitly require the size be 104 cards, and parametrized the game method on
 the dealer. We also added an additional test to verify the new deck size was
 being obeyed.

take5/patches/0004-deal-9-cards-instead-of-10.patch
For future maintainability, we added a constant for TURNS_PER_ROUND.

take5/patches/0005-increase-lowest-number-of-bull-points.patch
We changed our default strategy for assigning, our documentation, and fixed the 
 tests.

take5/patches/0006-change-player-to-place-lowest-card-first.patch
We changed the Player to play lowest card first and updated changed the tests
 accordingly.

take5/player.py
This file implements our new player based on the given strategy.

take5/player_tests.py
This file tests player.py.

player-protocol.txt
This file describes the communication protocol for the networked version of
 take5.
