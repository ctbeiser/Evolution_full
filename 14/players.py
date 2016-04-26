import sys

from evolution.player import *
from evolution.proxy_dealer import ProxyDealer
from evolution.json_socket import JSONSocket
from time import sleep

#Call with a number for player id, and a number for a port.

try:
    port = int(sys.argv[2])
except IndexError:
    port = 45678

index = 0
try:
    greeting = sys.argv[1]
    index = int(greeting)
except:
    greeting = "Hello"


#Make sure they're in order if we're passing an order.
sleep(index+1)
jsock = JSONSocket.from_host_and_port("localhost", port)
dealer = ProxyDealer(jsock, handshake=greeting)
dealer.begin()
