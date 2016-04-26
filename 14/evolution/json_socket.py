"""

Implements a StreamingJSONCoder that reads JSON messages from a
concatenated JSON stream and writes

"""

import json
import socket
from .timeout import *
from .debug import debug


class JSONSocket:
    """ Handles parsing of JSON objects from a concatenated JSON stream
    and writing JSON objects to the stream.
    """

    ENCODING = "utf-8"
    BYTE_SIZE = 1

    class IncompleteBufferException(ValueError):
        """ Raised when the buffer doesn't contain a full valid JSON bytestring """

    class ClosedSocketError(ValueError):
        """ Raised when the socket has been closed"""

    def __init__(self, sock):
        """ Initializes the decoder.
        :param sock : A socket.socket object that is initialized and connected.
        """
        self.buffer = bytes()
        self.sock = sock

    @classmethod
    def from_host_and_port(cls, host, port):
        """ Constructs a client JSONSocket from a host and a port number.
        :param host: String representing a hostname
        :param port: Integer representing a port number that can be connected to.
        :return: a JSONSocket
        Note: This method may find that the socket will not accept the connection. In that case, it will exit(1).
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            debug("The socket is in use")
            sock.close()
            exit(1)
        return cls(sock)

    @timeout(5)
    def decode(self):
        """ Retrieve a single JSON message from the socket if one can be retrieved
        This will not accept messages that take more than 3 seconds to arrive.
        :return: a single python-encoded JSON message
        Note: This method may throw a TimedOutError or a ClosedSocketError
        """
        return self.decode_without_timeout()

    def decode_without_timeout(self):
        """ A method that produces a message from the player as JSON
        INVARIANT: There will be a maximum of one message waiting
        :return: a python-encoded JSON message.
        Note: this message may run forever if the socket gets disconnected.
        """
        while True:
            # read byte-sized chunks
            data = self.sock.recv(self.BYTE_SIZE)

            if data:
                self.buffer += data
            else:
                raise self.ClosedSocketError
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
            debug(decoded, verbose=True)
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
        """ Encodes and sends the given object. Then, waits for a response to arrive.
        :param data: JSON data to encode and send.
        :return: JSON object
        This method may raise a ValueError if the other end doesn't send exactly one message within the allotted time.
        """
        self.encode(data)
        try:
            result = self.decode()
        except TimedOutError:
            debug("Decode timed out")
            debug(self.buffer)
            raise ValueError("No response arrived")
        # Ensure there's exactly one thing returned
        anything = self.sock.recv(self.BYTE_SIZE)
        if (anything and anything != b'\n' and anything != b' ' and anything != b'\t'):
            debug("Extra non-whitespace data was sent")
            raise ValueError("Invalid response from Player")
        return result

    def shutdown(self):
        """ Closes the socket connection
        :return: None
        """
        self.sock.close()