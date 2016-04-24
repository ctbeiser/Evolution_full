import socket
from .dealer import MAX_PLAYERS, MIN_PLAYERS
from .json_socket import JSONSocket
from .timeout import *
from .validate import *
from .debug import debug

class Server:
    """
    A Server holds a socket, allows players to connect, and conducts a handshake with them.
    """
    def __init__(self, host, port):
        """ Create a Server
        :param host: a String representing a hostname for a socket
        :param port: an Integer representing a port number.
        Note: If the port is already in use, this function will exit(1)
        """
        self.host = host
        self.port = port

        self.sock = self.initialize_socket()
        self.connected_players = []

    def add_players(self):
        """ Connect players to the Server until 8 have connected or the timer runs out
        :return: A list of players
        """
        while len(self.connected_players) < MIN_PLAYERS:
            try:
                self.check_for_new_players()
            except TimedOutError:
                pass
        self.add_to_8()
        return self.connected_players

    @timeout(5)
    def add_to_8(self):
        """
        Add players to the server until 8 have connected or the timer runs out
        :return:
        """
        while len(self.connected_players) < MAX_PLAYERS:
            try:
                self.check_for_new_players()
            except:
                break

    def check_for_new_players(self):
        x = self.blocking_call_to_socket_to_get_players()
        if x:
            clientsocket, addr = x
            self.add_new_player(clientsocket)

    @timeout(5)
    def blocking_call_to_socket_to_get_players(self):
        return self.sock.accept()

    def add_new_player(self, sock):
        player = JSONSocket(sock)
        info = player.decode()
        if is_string(info):
            player.encode("ok")
            self.connected_players.append(player)
        else:
            player.shutdown()

    def initialize_socket(self):
        """ Create a socket for listening for requests
        :return: a Socket.socket object, bound to the host and port of this server.
        Note: This function will exit(1) if the socket is in use.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((self.host, self.port))
        except ConnectionResetError:
            sock.close()
            debug("Server: Socket is already in use")
            exit(1)
        sock.listen(MAX_PLAYERS)
        return sock
