# Remote

## Directory

```
.                                   # Remote directory
├── Adapters/                       # Holds adapter classes
│   ├── logical_player_interface.py # A Player interface defined by the course.
│   ├── extended_referee.py         # Class extending the Referee class to add play_with(Colors[])
│   ├── logical_to_legacy_player.py # CoursePlayerInterface to PlayerInterface adapter class
│   └── legacy_to_logical_player.py # PlayerInterface to CoursePlayerInterface adapter class
├── Proxies/                        # Holds remote proxy classes
│   ├── json_stream.py              # JSONStream class, handles sending and receiving JSONs through file-like objects
│   ├── json_socket.py              # JSONSocket class, handles sending and receiving JSONs through a socket
│   ├── remote_player_proxy.py      # RemotePlayerProxy class, handles TCP communication with remote players
│   └── server_proxy.py             # ServerProxy class, handles TCP communication with Fish.com servers
├── Other/                          # Holds the test classes for adapter and proxy classes
├── client.py                       # A client for a remote player that connects to a server.
├── server.py                       # The FishServer class
├── xclient                         # Runnable that can create multiple clients
├── xserver                         # Runnable that creates and runs a Fish.com sign-up server and tournament
└── README.md                       # This README file
```

## Changes To Old Code
### Most Code
We reworked our import system to mitigate strange importing errors we saw relating to altering the Python import path. This resulted in a change in most of the module level import statements. We also added a Makefile for setting up and installing our project as a Python package. Some files also had their formatting fixed.

### Manager
We altered out manager to take a timeout attribute and abstracted out our `safe_call` function, which moved into `util.py`. We needed to rework all calls to the player in order to support handling player calls that take too long, a functionality that was missing. In addition the manager now returns a set of failing players from `run_tournament` so that our server can output the proper statistics.

### PlayerInterface
Our original PlayerInterface lacked `play_with` functionality, so this was added in in order to allow our referee to notify a player of his opponents. We also corrected some incorrect documentation.

### Referee
Referee was also changed to support our abstracted `safe_call` and thus player call timeout handling. We also added play-with functionality by extending the referee into our `ExtendedReferee` class.

### Action (Interface)
We added a `print_json` function to enable the serialization of Actions.

### Board
We added a `from_json` class method to enable the deserialization of Boards.

### constants.py
We added a default timeout constant for both our manager and referee to use. This is used primarily for `safe_call` calls to the player, again to implement missing functionality.

### Move
We implemented the `from_json` function. We also consolidated some documentation into the Action interface.

### PlayerData
We added a `from_json` class method to enable the deserialization of PlayerData (the player representation used by States).

### Skip
We altered the JSON representation of a Skip Action to match the correct course definition.

### State
We added a `from_json` class method to enable the deserialization of States.

### util.py
We added `is_posn` and `is_json_action` functions for validating JSONs sent by remote players. We also put our new `safe_call` functionality here.

### Player
We updated the return value of `tournament_end` to match the correct value defined by our original PlayerInterface.

## TODO

* [X] update legacy PlayerInterface
* [X] extend referee to broadcast player colors
    * [X] test that play_with is called
    * [X] kick players that dont respond correctly
* [X] update manager to use generic referee
    * [X] test interface enforcement
* [X] Asyncio passed to referee and manager
    * [X] test timeouts
* [X] create legacy -> course player adapter
    * [X] test call translation
* [X] create course -> legacy player adapter
    * [X] test call translation
* [X] create remote player proxy
    * [X] test
* [X] create server proxy
    * [X] test
* [X] create JSONStream that sends an receives JSONs
    * [X] test
* [X] create JSONSocket that sends an receives JSONs
    * [ ] test
* [X] create client that connects to server and creates server proxy / player
* [X] create xserver that signs up players and makes the tournament using player proxies
* [X] ensure that clients are shutdown properly
* [X] make sure default board parameters are correct
* [X] create xclient that creates multiple clients
* [X] ensure runnables are executable
* [X] test on khoury servers
* [ ] write about changes to old code
* [ ] create integration tests
