from Fish.Player.player import Player
from Fish.Remote.Adapters.logical_to_legacy_adapter import LogicalToLegacyPlayer
from Fish.Remote.Proxies.server_proxy import ServerProxy
from Fish.Remote.Proxies.json_socket import JSONSocket

import socket
import sys
import uuid


def main(address):
    """
    Create a remote Fish.com player and connect it to a
    Fish.com server at the given address.
    """
    print(address)
    name = '"' + uuid.uuid4().hex[:6].upper() + '"'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.sendall(name.encode())

    depth = 2
    player = Player(depth)
    adapter = LogicalToLegacyPlayer(player)
    server_proxy = ServerProxy(adapter, JSONSocket(sock))
    server_proxy.listen()
    sock.close()


if __name__ == '__main__':
    main((sys.argv[1], int(sys.argv[2])))
