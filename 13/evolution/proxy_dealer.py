from .streaming_json_coder import StreamingJSONCoder
from .validate import *
from .player import ExternalPlayer
from .timeout import *

class ProxyDealer:
    def __init__(self, coder):
        """ Validates JSON, unpacks it, and used it to call things on a Player.
        :param coder: A StreamingJsonCoder
        """
        self.player = ExternalPlayer(0)
        self.coder = coder
        self.coder.encode("Hello")

    def begin(self):
        self.wait_for_ok()
        self.update_for_start()
        while True:
            self.wait_for_choice_request()
            self.wait_for_feed_species_and_restart()

    def wait_for_ok(self):
        try:
            result = self.coder.decode_without_timeout()
            if not result == "ok":
                raise ValueError()
        except:
            self.coder.shutdown()
            exit(1)

    def update_for_start(self):
        try:
            result = self.coder.decode_without_timeout()
            self.player.rehydrate_from_state_without_others(result)
        except:
            self.coder.shutdown()
            exit(1)

    def wait_for_choice_request(self):
        try:
            request = self.coder.decode_without_timeout()
            response = self.player.choose(request[0], request[1])
            self.coder.encode(response)
        except:
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
            self.coder.shutdown()
            exit(1)