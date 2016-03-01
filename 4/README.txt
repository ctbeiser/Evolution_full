This projects implements a remote player client, which wraps our Player
 implementation from assignment 3 and communicates with a game server
 over TCP. The project also includes a design document for the Evolution
 game.

remote/remote-client
executable file that launches the remote player client

remote/remote_player.py
implements the remote player

remote/streaming_json_coder.py
implements a coder that handles the communication with the server though
JSON messages over a TCP connection

remote/test_remote_player.py
tests for the remote player

remote//test_streaming_json_coder.py
tests for the streaming JSON coder

test/{number}-in.json
messages to be send a remote player for testing

test/{number}-out.json
expected responses to messages in {number}-in.json

evolution/documentation.txt
documents the structure and the ambiguities found in the requirements analysis
of the evolution game

evolution/components.png
structure of the components of the evolution game