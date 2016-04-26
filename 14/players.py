import sys

from evolution.player import *
from evolution.proxy_dealer import ProxyDealer
from evolution.json_socket import JSONSocket
from time import sleep

port = 45678
try:
    port = int(sys.argv[1])
    greeting = sys.argv[2]
    id = int(greeting)
except:
    greeting = "Hello"
    id = 1

#Make sure they're in order if we're passing an order.
sleep(id)
jsock = JSONSocket.from_host_and_port("localhost", port)
dealer = ProxyDealer(jsock, handshake=greeting)
dealer.begin()
