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
        # The listener socket for this server— a socket.Socket object
        self.sock = self.initialize_socket(host, port)
        # A list of (JSONSocket, String) representing the socket for a player and their handshake message
        self.connected_players = []

    def add_players(self):
        """ Connect players to the Server until at least the minimum have connected, and up to the maximum have
        :return: A list of (JSONSockets mapping to each player.
        """
        while len(self.connected_players) < MIN_PLAYERS:
            try:
                self.check_for_new_players()
            except TimedOutError:
                pass
        self.add_to_max()
        return self.connected_players

    @timeout(5)
    def add_to_max(self):
        """ Add more players to the server until 8 have connected or the timer runs out. It
        """
        while len(self.connected_players) < MAX_PLAYERS:
            try:
                self.check_for_new_players()
            except:
                break

    def check_for_new_players(self):
        """ Check whether there are new players waiting to connect,
        adds players the the list of connected players.
        """
        x = self.blocking_call_to_socket_to_get_players()
        if x:
            clientsocket, addr = x
            self.add_new_player(clientsocket)

    @timeout(5)
    def blocking_call_to_socket_to_get_players(self):
        """ Calls accept on the socket to get new players. It's necessary to break this out to make it impossible for
        the timeout to interrupt after we've had the handshake with the player.
        :return: a Socket.socket client socket.
        Note: this will throw a TimedOutError if there's no player to get
        """
        return self.sock.accept()

    def add_new_player(self, sock):
        """ Create a JSONSocket for this socket, conduct a handshake, and add it to the list of players for this player
        :param sock: a Socket.socket client socket
        """
        player = JSONSocket(sock)
        info = player.decode()
        if is_string(info):
            player.encode("ok")
            self.connected_players.append(player, info)
        else:
            player.shutdown()

    def initialize_socket(self, host, port):
        """ Create a socket for listening for requests
        :param host: a String representing a hostname
        :param port: an Integer representing the port to listen on
        :return: a Socket.socket server socket
        Note: This function will exit(1) if the socket is in use.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # It is necessary to pass this function a Tuple of (Host, Port) because the API authors thought that
            # it was more important to mirror over how this was done in C than make something sane
            sock.bind((host, port))
        except ConnectionResetError:
            sock.close()
            debug("Server: Socket is already in use")
            exit(1)
        sock.listen(MAX_PLAYERS)
        return sock
