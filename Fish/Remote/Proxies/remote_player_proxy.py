from Fish.Remote.Adapters.logical_player_interface import LogicalPlayerInterface
from Fish.Remote.Proxies.json_stream import JSONStream
from Fish.Common.action import Action
from Fish.Common.util import is_posn

class RemotePlayerProxy(LogicalPlayerInterface):
    """
    uses a JSONstream to communicate with a remote player. The RemotePlayerProxy will write to the JSONstream to send requests to the 
    player and read from the stream to get the player response. 

    self.__json_stream: the JSONstream object that we will use to make remote calls to the remote player
    """

    def __init__(self, json_stream):
        """
        Creates a RemotePlayerProxy that will act as a Proxy to a remote Player.
        Calls to the remote player will be sent over the JSONstream object.

        JSONstream -> RemotePlayerProxy
        """

        self.__json_stream = json_stream

    def __send_request(self, name, args, validate, error):
        """
        Sends a request to the remote player and looks for a response. 
        If the method does not return a value the string "void" is expected
        The arguments to this function are described in the Remote Interactions

        String, [List-of Any] -> "void" | Position | Action
        """
        
        self.__json_stream.send_json([name, args])
        response = self.__json_stream.recv_json()
        
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
        self.__send_request("playing-as", [color], self.__resp_is_void, error)

    def play_with(self, colors):
        error = "Player did not return 'void' to play_with method"
        self.__send_request("playing-with", [colors], self.__resp_is_void, error)

    def setup(self, state):
        error = "Player did not return a int, int tuple to setup method"
        return self.__send_request("setup", [state], is_posn, error)

    def tt(self, state, actions):
        validate = lambda resp : isinstance(resp, Action)
        error = "Player did not return an Action to tt method"
        return self.__send_request("take-turn", [state, actions], validate, error)