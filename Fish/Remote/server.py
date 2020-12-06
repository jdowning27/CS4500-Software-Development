from Fish.Admin.manager import Manager
from Fish.Remote.Adapters.legacy_to_logical_player import LegacyToLogicalPlayer
from Fish.Remote.Proxies.remote_player_proxy import RemotePlayerProxy
from Fish.Remote.Proxies.json_socket import JSONSocket

import select
import socket
from time import time


class FishServer():
    """
    Fish.com server that signs up players and runs a tournament.

    self.lsock:         The server's TCP listening socket
    self.players:       A list of signed up RemotePlayerProxies
    self.player_socks:  A list the player's client sockets
    """

    MIN_PLAYERS = 5
    MAX_PLAYERS = 10
    WAITING_PERIOD = 5  # 30
    NUM_WAITING_PERIODS = 2
    BOARD_CONFIG = {"row": 5, "col": 5, "fish": 2}

    def __init__(self, address):
        """
        Create a new FishServer.

        (IP Address, port) -> FishServer
        """
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind(address)
        self.lsock.listen(FishServer.MAX_PLAYERS)
        self.players = []
        self.player_socks = []

    def get_players(self):
        """
        Get a list of signed up RemotePlayerProxies.

        Void -> [List-of RemotePlayerProxy]
        """
        return self.players

    def handle_request(self):
        """
        Handle a single connection request, adding that player to the signup list.

        Void -> Void
        """
        ready_to_read, ready_to_write, in_error = select.select([self.lsock], [], [], 0.1)
        if self.lsock in ready_to_read:
            csock, addr = self.lsock.accept()
            json_sock = JSONSocket(csock)
            json_sock.recv_json()   # receive the name of the player, nothing to do with it
            rpp = LegacyToLogicalPlayer(RemotePlayerProxy(json_sock))
            self.players.append(rpp)
            self.player_socks.append(csock)

    def run_signup(self):
        """
        Run the tournament signup. Wait for players for WAITING_PERIOD.
        If there are more that MIN_PLAYERS after this, return True.
        Otherwise, wait for one more period. If there are enough player,
        return True. If at any point there are MAX_PLAYERS signed up,
        return True.

        Void -> Boolean
        """
        waiting_periods = 1
        start_time = time()
        while True:
            self.handle_request()
            if len(self.players) >= FishServer.MAX_PLAYERS:
                return True
            if time() - start_time >= FishServer.WAITING_PERIOD:
                # print('period')
                if len(self.players) >= FishServer.MIN_PLAYERS:
                    return True
                elif waiting_periods >= FishServer.NUM_WAITING_PERIODS:
                    return False
                else:
                    waiting_periods += 1
                    start_time = time()

    def run_tournament(self):
        """
        Run a tournament with all signed up players.

        Void -> Void
        """
        winners, cheaters = Manager().run_tournament(self.players, FishServer.BOARD_CONFIG)
        print(f"[{len(winners)}, {len(cheaters)}]")

    def shutdown(self):
        """
        Shutdown the server by closing all sockets.

        Void -> Void
        """
        self.lsock.shutdown(socket.SHUT_RDWR)
        self.lsock.close()
        for sock in self.player_socks:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
