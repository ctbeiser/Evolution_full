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
            self.wait_for_feed_species()

    def wait_for_ok(self):
        try:
            print("trying wait ok")
            result = self.coder.decode_without_timeout()
            if not result == "ok":
                raise ValueError()
        except (TimedOutError, ValueError):
            print("failed OK")
            exit()

    def update_for_start(self):
        try:
            print("trying update start")
            result = self.coder.decode_without_timeout()
            self.player.rehydrate_from_state_without_others(result)
        except (TimedOutError, ValueError):
            print("waiting for start")
            exit()

    def wait_for_choice_request(self):
        try:
            print("trying wait choice req")
            request = self.coder.decode_without_timeout()
            response = self.player.choose(request[0], request[1])
            print(response)
            self.coder.encode(response)
            print("sent")
        except (TimedOutError, ValueError):
            print("Timeout")
            exit()

    def wait_for_feed_species(self):
        try:
            print("trying wait for feed")
            request = self.coder.decode_without_timeout()
            self.coder.encode(self.player.feed_species(request))
        except (TimedOutError, ValueError):
            print("notfed")
            exit()