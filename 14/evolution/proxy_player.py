class ProxyPlayer:
    """A Player that follows the interface for an External Player, but connects with an agent across a JSONSocket"""

    def __init__(self, jsock):
        """ Creates a player that acts as an ExternalPlayer, by connecting to it remotely using a StreamingJsonCoder
        :param jsock:
        """
        self.jsock = jsock

    # The following three method's signatures represent the

    def start(self, msg):
        """ Given a JSON message representing a message to start the game, send it to the remote player
        :param msg: a JSON message
        """
        self.jsock.encode(msg)

    def choose(self, before, after):
        """ Ask the remote player to choose the actions to take based on state and the players before and after
        :param before: a list of Player as JSON
        :param after: a list of Player as JSON
        :return: a Action4 as JSON
        Note: This message will raise a ValueError if the agent doesn't conform to the protocol.
        """
        try:
            json_response = self.jsock.send_and_get_response([before, after])
            return json_response
        except ConnectionResetError:
            raise ValueError()

    def feed_species(self, state):
        """ Ask the remote player to feed the species
        :param state: A python-encoded JSON State
        :return: a python-encoded FeedingIntent
        Note: This message will raise a ValueError if the agent doesn't conform to the protocol.
        """
        try:
            maybe_raw_json_response = self.jsock.send_and_get_response(state)
            return maybe_raw_json_response
        except ConnectionResetError:
            raise ValueError()
