import json


class JSONStream():
    """
    Wraps read and write streams from sending and receiving JSONs.

    Any multi-digit number sent outside of another JSON element
    (e.g. parentheses, quotes, brackets),
    will be misinterpreted as multiple single digit numbers:
    (e.g. 123 -> 1, 2, 3).

    self.__rfile:  File-like for reading.
    self.__wrfile: File-like for writing.
    """

    def __init__(self, rfile, wfile):
        """
        Initialize a JSONStream.

        File-like, File-like -> JSONStream
        """
        self.__rfile = rfile
        self.__wfile = wfile
        self.__decoder = json.JSONDecoder()
        self.__encoder = json.JSONEncoder()

    def recv_json(self):
        """
        Receive a JSON value in python representation from the stream.
        Blocks until a full JSON value is received.

        Void -> JSON value
        """
        buffer = ""
        while True:
            try:
                buffer += self.__rfile.read(1)
                if len(buffer) > 0:
                    print(buffer)
                return self.__decoder.raw_decode(buffer)[0]
            except json.decoder.JSONDecodeError:
                pass

    def send_json(self, value):
        """
        Send a JSON value in python representation over the stream.

        JSON value -> Void
        """
        self.__wfile.write(self.__encoder.encode(value))
