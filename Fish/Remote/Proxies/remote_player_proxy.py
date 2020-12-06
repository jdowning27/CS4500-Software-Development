from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface
from Fish.Remote.Proxies.json_socket import JSONSocket
from Fish.Common.action import Action
from Fish.Common.move import Move
from Fish.Common.skip import Skip
from Fish.Common.util import is_posn, is_json_action


class RemotePlayerProxy(LogicalPlayerInterface):
    """
    uses a JSONSocket to communicate with a remote player. The RemotePlayerProxy will write to the JSONSocket to send requests to the
    player and read from the sock to get the player response.

    self.__json_sock: the JSONSocket object that we will use to make remote calls to the remote player
    """

    def __init__(self, json_sock):
        """
        Creates a RemotePlayerProxy that will act as a Proxy to a remote Player.
        Calls to the remote player will be sent over the JSONSocket object.

        JSONSocket -> RemotePlayerProxy
        """
        if not isinstance(json_sock, JSONSocket):
            raise ValueError("json_sock must be an instance of JSONSocket")

        self.__json_sock = json_sock

    def __send_request(self, name, args, validate, error):
        """
        Sends a request to the remote player and looks for a response.
        If the method does not return a value the string "void" is expected
        The arguments to this function are described in the Remote Interactions

        String, [List-of Any] -> "void" | Position | Action
        """

        self.__json_sock.send_json([name, args])
        response = self.__json_sock.recv_json()

        if not validate(response):
            raise RuntimeError(error)
        return response

    def __resp_is_void(self, resp):
        return resp == "void"

    def start(self, starting):
        error = "Player did not return 'void' to start method"
        self.__send_request("start", [starting], self.__resp_is_void, error)

    def end(self, did_win):
        error = "Player did not return 'void' to end method"
        self.__send_request("end", [did_win], self.__resp_is_void, error)

    def play_as(self, color):
        error = "Player did not return 'void' to play_as method"
        self.__send_request("playing-as", [color.value], self.__resp_is_void, error)

    def play_with(self, colors):
        error = "Player did not return 'void' to play_with method"
        self.__send_request("playing-with", [[color.value for color in colors]],
                            self.__resp_is_void, error)

    def setup(self, state):
        error = "Player did not return an int, int 2-tuple to setup method"
        return tuple(self.__send_request("setup", [state.print_json()], is_posn, error))

    def tt(self, state, actions):
        error = "Player did not return an Action to tt method"
        actions = [action.print_json() for action in actions]
        response = self.__send_request("take-turn", [state.print_json(), actions],
                                       is_json_action, error)
        if response is False:
            return Skip()
        else:
            return Move.from_json(response)
