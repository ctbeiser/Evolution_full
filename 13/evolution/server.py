import socket
from .dealer import MAX_PLAYERS
from .streaming_json_coder import StreamingJSONCoder
from .timeout import timeout
from .validate import *


class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = self.initialize_socket()
        self.connected_players = []

    def add_players(self):
        while len(self.connected_players) < 3:
            print("trying")
            try:
                self.check_for_new_players()
            except:
                pass
        self.add_to_8()
        return self.connected_players

    @timeout(5)
    def add_to_8(self):
        print("that's three")
        while len(self.connected_players) < 8:
            try:
                print("trian")
                self.check_for_new_players()
            except:
                break

    def check_for_new_players(self):
        x = self.blocking_call_to_socket_to_get_players()
        if x:
            clientsocket, addr = x
            print('Incoming connection from %s' % repr(addr))
            self.add_new_player(clientsocket)

    @timeout(5)
    def blocking_call_to_socket_to_get_players(self):
        return self.sock.accept()

    def add_new_player(self, sock):
        player = StreamingJSONCoder(sock)
        info = player.decode()
        if is_string(info):
            player.encode("ok")
            print("ok")
            self.connected_players.append(player)
        else:
            player.shutdown()

    def initialize_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(MAX_PLAYERS)
        return sock
