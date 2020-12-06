import json
import socket


class JSONSocket():
    """
    Wraps a socket for sending and receiving JSONs.

    Any multi-digit number sent outside of another JSON element
    (e.g. parentheses, quotes, brackets),
    will be misinterpreted as multiple single digit numbers:
    (e.g. 123 -> 1, 2, 3).

    self.__sock:    socket for communicating over
    self.__json_decoder: JSON decoder
    self.__json_encoder: JSON encoder
    """

    def __init__(self, sock):
        """
        Initialize a JSONSocket.

        socket -> JSONSocket
        """
        sock.settimeout(0.1)
        self.__sock = sock
        self.__json_decoder = json.JSONDecoder()
        self.__json_encoder = json.JSONEncoder()

    def recv_json(self):
        """
        Receive a JSON value in python representation from the socket.
        Blocks until a full JSON value is received.

        Returns None if the connection has closed.

        Void -> Maybe JSON value
        """
        buffer = ""
        while True:
            if self.__sock.fileno() == -1:
                return None
            try:
                byte = self.__sock.recv(1)
                buffer += byte.decode()
                val = self.__json_decoder.raw_decode(buffer)[0]
                print(val)
                break
            except (json.decoder.JSONDecodeError, socket.timeout):
                pass
        return val

    def send_json(self, value):
        """
        Send a JSON value in python representation over the socket.

        JSON value -> Void
        """
        self.__sock.sendall(self.__json_encoder.encode(value).encode())
