"""

Implements a StreamingJSONCoder that reads JSON messages from a
concatenated JSON stream and writes

"""

import json
import socket
from .dealer import MAX_PLAYERS
from .timeout import *


class StreamingJSONCoder:
    """ Handles parsing of JSON objects from a concatenated JSON stream
    and writing JSON objects to the stream.
    """

    ENCODING = "utf-8"
    BYTE_SIZE = 1

    class IncompleteBufferException(ValueError):
        """ Raised when the buffer doesn't contain a full valid JSON bytestring """

    def __init__(self, sock):
        """ Initializes the decoder.
        :param host: stream host as a string
        :param port: stream port as an integer
        """
        self.buffer = bytes()
        self.sock = sock

    @timeout(3)
    def decode(self):
        return self.decode_without_timeout()

    def decode_without_timeout(self):
        """ A method that produces a message from the player as JSON
        INVARIANT: There will be a maximum of one message waiting
        :return:
        """
        while True:
            # read byte-sized chunks
            data = self.sock.recv(self.BYTE_SIZE)

            if data:
                self.buffer += data
            try:
                parsed = self.parse_buffer()
                return parsed
            except self.IncompleteBufferException:
                pass

    def parse_buffer(self):
        """ Parses the current buffer, if a valid JSON object is decoded
        it is returned, otherwise returns None
        :return: JSON object or None
        """
        try:
            decoded = json.loads(self.buffer.decode(self.ENCODING))
            self.buffer = bytes()
            return decoded
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise self.IncompleteBufferException()

    def encode(self, data):
        """ Encodes and sends the given object to the stream.
        :param data: JSON data to encode and send to the stream
        """
        encoded_data = json.dumps(data).encode(self.ENCODING)
        self.sock.sendall(encoded_data + b'\n')

    def send_and_get_response(self, data):
        self.encode(data)
        try:
            result = self.decode()
        except TimedOutError:
            raise ValueError("No response arrived")
        # Ensure there's exactly one thing returned
        anything = self.sock.recv(self.BYTE_SIZE)
        if (anything and anything != b'\n') or not result:
            raise ValueError("Invalid response from Player")
        return result

    def shutdown(self):
        """ Closes the socket connection
        :return: None
        """
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
