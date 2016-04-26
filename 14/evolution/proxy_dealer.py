from .json_socket import JSONSocket
from .validate import *
from .player import ExternalPlayer
from .timeout import *
from .debug import debug
from .json_socket import JSONSocket

class ProxyDealer:
    """ Implements a finite state machine of the messages acceptable by the Player, and sends responses from
        an ExternalPlayer"""
    def __init__(self, coder, player=None, handshake="Hello"):
        """ Creates a ProxyDealer, and sends an initial handshake to it.
        :param coder: a JSONSocket connected to a server
        :param player: Optionally, a class to use as a player agent. If none is found,
        :param handshake: a String to send as a handshake to the Server
        """
        self.player = player or ExternalPlayer(0)
        self.coder = coder
        self.coder.encode(handshake)

    def begin(self):
        """ the main loop of the Dealer. Wait for, process, and respond to messages from the client
        Note: This function is crash-only; it will not return.
        """
        try:
            self.wait_for_ok()
            self.update_for_start()
            while True:
                self.wait_for_choice_request()
                self.wait_for_feed_species_and_restart()
        except JSONSocket.ClosedSocketError:
            self.coder.shutdown()
            debug("The port has shut down")
            exit(1)


    def wait_for_ok(self):
        """ Verify the handshake from the dealer. If it isn't 'ok', quit the application.
        """
        result = self.coder.decode_without_timeout()
        if not result == "ok":
            debug("We've received something other than an 'ok' in the handshake.")
            self.coder.shutdown()
            exit(1)


    def update_for_start(self):
        """ Represents the state of the DFA for the dealer where it must send a start-round message,
        translates that to the player agent.
        """
        try:
            result = self.coder.decode_without_timeout()
            self.player.start(result)
        except ValueError:
            debug("Updating for the start of the round has failed")
            self.coder.shutdown()
            exit(1)

    def wait_for_choice_request(self):
        """ Represents the state of the DFA for the dealer where it must receive a 'choose-feeding-intent' message,
            translates that to the player agent.
        """
        try:
            request = self.coder.decode_without_timeout()
            response = self.player.choose(request[0], request[1])
            self.coder.encode(response)
        except ValueError:
            debug("Choosing cards has failed")
            self.coder.shutdown()
            exit(1)

    def wait_for_feed_species_and_restart(self):
        """ Represents the state of the DFA for the dealer where it may receive a feeding message, but it may also
            receive a new-round message, and translates that to the plaer agent.
        """
        try:
            while True:
                request = self.coder.decode_without_timeout()
                if len(request) == 4:
                    self.player.start(request)
                    return
                else:
                    self.coder.encode(self.player.feed_species(request))
        except ValueError:
            debug("Feeding has failed")
            self.coder.shutdown()
            exit(1)