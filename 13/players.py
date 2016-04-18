from evolution.player import *
from evolution.proxy_dealer import ProxyDealer
from evolution.streaming_json_coder import StreamingJSONCoder
from time import sleep
import socket
import sys

def initialize_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


sleep(1)
coder = StreamingJSONCoder(initialize_socket("localhost", 45678))
dealer = ProxyDealer(coder)
dealer.begin()


