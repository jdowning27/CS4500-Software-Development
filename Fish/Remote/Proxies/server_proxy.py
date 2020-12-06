from Fish.Common.color import Color
from Fish.Common.move import Move
from Fish.Common.state import State
from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface
from Fish.Remote.Proxies.json_socket import JSONSocket


class ServerProxy():
    """
    Proxy for communicating with a Fish.com server as a player over the internet.

    When listen() is called, the ServerProxy will run a loop that listens for incoming messages,
    decodes them, and makes the appropriate call the self.__player. This will continue and block
    until the tournament has ended or the connection is closed.

    self.__player:              A LogicalPlayerInterface object representing the player
    self.__json_sock:           A JSONSocket for sending and receiving messages
    self.__request_handlers:    A dictionary of message handler functions
                                corresponding to each message type
    """

    def __init__(self, player, json_sock):
        """
        Initialize a ServerProxy.

        LogicalPlayerInterface, JSONSocket -> ServerProxy
        """
        if not isinstance(player, LogicalPlayerInterface):
            raise ValueError("player must be an instance of LogicalPlayerInterface")

        if not isinstance(json_sock, JSONSocket):
            raise ValueError("json_sock must be an instance of JSONSocket")

        self.__player = player
        self.__json_sock = json_sock

        self.__request_handlers = {
            "start":        self.__handle_start,
            "playing-as":   self.__handle_play_as,
            "playing-with": self.__handle_playing_with,
            "setup":        self.__handle_setup,
            "take-turn":    self.__handle_take_turn,
            "end":          self.__handle_end
        }

    def listen(self):
        while True:
            request = self.__json_sock.recv_json()
            if request is None:
                break
            response = self.__handle_request(request)
            self.__json_sock.send_json(response)
            if request is None or request[0] == "end":
                break

    def __handle_request(self, request):
        """
        Handle a JSON request and return the player's response.

        JSON value -> JSON value
        """
        name, arguments = request
        return self.__request_handlers[name](arguments)

    def __handle_start(self, arguments):
        """
        Handle a start message.

        JSON value -> JSON value
        """
        self.__player.start(arguments[0])
        return "void"

    def __handle_play_as(self, arguments):
        """
        Handle a start message.

        JSON value -> JSON value
        """
        self.__player.play_as(Color(arguments[0]))
        return "void"

    def __handle_playing_with(self, arguments):
        """
        Handle a start message.

        JSON value -> JSON value
        """
        self.__player.play_with([Color(arg) for arg in arguments[0]])
        return "void"

    def __handle_setup(self, arguments):
        """
        Handle a start message.

        JSON value -> JSON value
        """
        state = State.from_json(arguments[0])
        return self.__player.setup(state)

    def __handle_take_turn(self, arguments):
        """
        Handle a start message.

        JSON value -> JSON value
        """
        state = State.from_json(arguments[0])
        actions = [Move.from_json(action) for action in arguments[1]]
        return self.__player.tt(state, actions).print_json()

    def __handle_end(self, arguments):
        """
        Handle a start message.

        JSON value -> JSON value
        """
        self.__player.end(arguments[0])
        return "void"
