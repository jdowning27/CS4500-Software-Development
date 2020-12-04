class JSONStream():
    """
    Wraps read and write streams from sending and receiving JSONs.

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
        pass

    def recv_json(self):
        """
        Receive a JSON value in python representation from the stream.
        Blocks until a full JSON value is received.

        Void -> JSON value
        """
        pass

    def send_json(self, value):
        """
        Send a JSON value in python representation over the stream.

        JSON value -> Void
        """
        pass
