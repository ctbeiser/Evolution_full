from evolution.player import *
from evolution.proxy_dealer import ProxyDealer
from evolution.json_socket import JSONSocket
from time import sleep

sleep(1)
jsock = JSONSocket.from_host_and_port("localhost", 45678)
dealer = ProxyDealer(jsock)
dealer.begin()
