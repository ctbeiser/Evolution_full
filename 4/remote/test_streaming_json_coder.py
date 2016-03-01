import json
import unittest
import unittest.mock

from streaming_json_coder import StreamingJSONCoder


class StreamingJsonCoderTestCase(unittest.TestCase):

    def setUp(self):
        with unittest.mock.patch("streaming_json_coder.socket", return_value=unittest.mock.MagicMock):
            self.coder = StreamingJSONCoder("localhost", "45678")

        self.test_strings = [
            True,
            None,
            {},
            "string",
            {'dict': 'value'},
            [],
            ["one", "two"],
        ]

    def test_decode(self):

        self.coder.sock.recv.return_value = None
        with self.assertRaises(StopIteration):
            self.coder.decode().__next__()

        def test_receive_data(sent_data):
            # sent data byte by byte
            sent_data_string = json.dumps(sent_data).encode(self.coder.ENCODING)
            self.coder.sock.recv.side_effect = [bytes([b]) for b in sent_data_string]

            for decoded_data in self.coder.decode():
                self.assertEqual(decoded_data, sent_data)
                # buffer should now be empty
                self.assertEqual(self.coder.buffer, bytes())

        for sent_data in self.test_strings:
            test_receive_data(sent_data)

    def test_parse_buffer(self):
        """ Tests that the nothing happens if the buffer contains only a part
        of a JSON string, but as soon as a JSON object can be decoded returns
        the object and clears the buffer.
        """
        for buffer_value in self.test_strings:
            buffer_value_string = json.dumps(buffer_value).encode(self.coder.ENCODING)

            self.coder.buffer = bytes()
            for byte in buffer_value_string:
                self.coder.buffer += bytes(byte)
                if len(self.coder.buffer) == len(buffer_value_string):
                    self.assertEqual(self.coder.parse_buffer(), buffer_value)
                    self.assertEqual(self.coder.buffer, bytes())
                else:
                    with self.assertRaises(StreamingJSONCoder.IncompleteBufferException):
                        self.coder.parse_buffer()

    def test_encode(self):

        for data in self.test_strings:
            self.coder.encode(data)

            encoded_data = json.dumps(data).encode(self.coder.ENCODING)
            self.coder.sock.sendall.assert_called_once_with(encoded_data)
            self.coder.sock.reset_mock()

    def test_shutdown(self):

        self.coder.shutdown()
        self.assertTrue(self.coder.sock.shutdown.called)
        self.assertTrue(self.coder.sock.close.called)

    def test_decode_list(self):
        to_send_string = "".join(json.dumps(string) for string in self.test_strings)
        to_send_encoded = to_send_string.encode(self.coder.ENCODING)

        self.coder.sock.recv.side_effect = [bytes([b]) for b in to_send_encoded]
        decoded_strings = [decoded_string for decoded_string in self.coder.decode()]
        self.assertListEqual(decoded_strings, self.test_strings)

