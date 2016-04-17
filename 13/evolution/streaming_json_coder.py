"""

Implements a StreamingJSONCoder that reads JSON messages from a
concatenated JSON stream and writes

"""

import json
import socket


class StreamingJSONCoder:
    """ Handles parsing of JSON objects from a concatenated JSON stream
    and writing JSON objects to the stream.
    """

    ENCODING = "utf-8"
    BYTE_SIZE = 1

    class IncompleteBufferException(ValueError):
        """ Raised when the buffer doesn't contain a full valid JSON bytestring """

    def __init__(self, host, port):
        """ Initializes the decoder.
        :param host: stream host as a string
        :param port: stream port as an integer
        """
        self.host = host
        self.port = port

        self.buffer = bytes()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def decode(self):
        """ A generator method that continuously returns parsed JSON
        objects until the connection is broken.
        INVARIANT from the project description: the data sent is valid JSON
        :return:
        """
        while True:
            # read byte-sized chunks
            data = self.sock.recv(self.BYTE_SIZE)

            if data:
                self.buffer += data
            else:
                raise StopIteration()

            try:
                parsed = self.parse_buffer()
                yield parsed
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

    def shutdown(self):
        """ Closes the socket connection
        :return: None
        """
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
