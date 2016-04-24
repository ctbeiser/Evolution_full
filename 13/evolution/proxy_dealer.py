from .json_socket import JSONSocket
from .validate import *
from .player import ExternalPlayer
from .timeout import *
from .debug import debug

class ProxyDealer:
    """ Implements a finite state machine of the messages acceptable by the Player, and sends responses from
        an ExternalPlayer"""
    def __init__(self, coder, player=None, greeting="Hello"):
        """ Creates a ProxyDealer, and sends an initial handshake to it.
        :param coder: a JSONSocket connected to a server
        :param player: Optionally, a class to use as a player agent. If none is found,
        :param greeting: a String to send as a handshake to the Server
        """
        self.player = player or ExternalPlayer(0)
        self.coder = coder
        self.coder.encode(greeting)

    def begin(self):
        """ the main loop of the Dealer. Wait for, process, and respond to messages from the
        :return:
        """
        self.wait_for_ok()
        self.update_for_start()
        while True:
            self.wait_for_choice_request()
            self.wait_for_feed_species_and_restart()


    def wait_for_ok(self):
        result = self.coder.decode_without_timeout()
        if not result == "ok":
            debug("We've received something other than an 'ok' in the handshake.")
            raise ValueError()


    def update_for_start(self):
        """
        :return:
        """
        try:
            result = self.coder.decode_without_timeout()
            self.player.rehydrate_from_state_without_others(result)
        except:
            debug("Updating for the start of the round has failed")
            self.coder.shutdown()
            exit(1)

    def wait_for_choice_request(self):
        try:
            request = self.coder.decode_without_timeout()
            response = self.player.choose(request[0], request[1])
            self.coder.encode(response)
        except:
            debug("Choosing cards has failed")
            self.coder.shutdown()
            exit(1)

    def wait_for_feed_species_and_restart(self):
        try:
            while True:
                request = self.coder.decode_without_timeout()
                if len(request) == 3:
                    self.player.rehydrate_from_state_without_others(request)
                    return
                else:
                    self.coder.encode(self.player.feed_species(request))
        except:
            debug("Feeding has failed")
            self.coder.shutdown()
            exit(1)