import sys

from evolution.player import *
from evolution.proxy_dealer import ProxyDealer
from evolution.json_socket import JSONSocket
from time import sleep

try:
    port = int(sys.argv[1])
except IndexError:
    port = 45678

sleep(1)
jsock = JSONSocket.from_host_and_port("localhost", port)
dealer = ProxyDealer(jsock)
dealer.begin()
