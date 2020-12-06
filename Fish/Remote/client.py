from Fish.Player.player import Player
from Fish.Remote.Adapters.logical_to_legacy_adapter import LogicalToLegacyPlayer
from Fish.Remote.Proxies.server_proxy import ServerProxy
from Fish.Remote.Proxies.json_stream import JSONStream

import socket
import sys
import uuid


def main(port):
    """
    Create a remote Fish.com player and connect it to a
    Fish.com server on localhost through the given port.
    """
    name = '"' + uuid.uuid4().hex[:6].upper() + '"'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', port))
    sock.sendall(name.encode())

    depth = 2
    player = Player(depth)
    adapter = LogicalToLegacyPlayer(player)
    server_proxy = ServerProxy(adapter, JSONStream(sock.makefile('r'), sock.makefile('w')))
    server_proxy.listen()
    sock.close()


if __name__ == '__main__':
    main(int(sys.argv[1]))
