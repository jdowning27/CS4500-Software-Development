# Remote Planning

## Logical Interaction Diagram
```
  Players           Fish.com Server         Tournament Manager          Referee
    +                       +                        +                     +
    |    Sign-up Request    |                        |                     |
*1  | +-------------------> |   Run Tournament w/    |                     |
    | Confirmation/Waitlist |   Players              |                     |
*2  | <-------------------+ | +--------------------> |                     |
    |                       |                        |                     |
    |                       |    Start Tournament    |                     |
*3  | <--------------------------------------------+ |                     |
    |    Ready to start     |                        |    Runs N rounds    | <-----------------------+
*4  | +--------------------------------------------> |    of Games         |                         |
    |                       |                        | +-----------------> |                         |
    |                       |                        |                     |                         |
    |                       |                        |   Assign Colors     |                         |
*5  | <------------------------------------------------------------------+ |                         |
    |                       |                        |                     |                         |
    |                       |                        |  Request Penguin    |                         |
    |                       |                        |  Placements         |                         |
*6  | <------------------------------------------------------------------+ |                         |
    |                       |                        |                     |                         |
    | Respond w/ Placement  |                        |                     |                         |
    | Coordinate            |                        |                     |                         |
*7  | +------------------------------------------------------------------> |                         |
    |                       |                        |                     |                         |
    |                       |                        |  Broadcast Starting |                         |
    |                       |                        |  Game State         |                         |
*8  | <------------------------------------------------------------------+ |                         |
    |                       |                        |                     |                         |
    |                       |                        |  Request Moves      | <---------------------+ |
*9  | <------------------------------------------------------------------+ |                       | |
    |                       |                        |                     |                       | |
    |  Respond w/ Moves     |                        |                     |                       | |
*10 | +------------------------------------------------------------------> |                       | |
    |                       |                        |                     |                       | |
    |                       |                        |  Broadcast Actions  |   If Failing Player   | |
*11 | <------------------------------------------------------------------+ |   kick them and       | |
    |                       |                        |                     |   Broadcast new State | |
    |                       |                        |                     |                       | |
    |                       |                        |                     |   Repeat until  +-----+ |
    |                       |                        |                     |   Game Over             |
    |                       |                        | Broadcast Game Over |                         |
*12 | <------------------------------------------------------------------+ |                         |
    |                       |                        |                     |                         |
    |                       |                        |  Return Game Results|                         |
    |                       |                        | <-----------------+ |                         |
    |                       |                        |                     |                         |
    |                       |                        |  Repeat until       |                         |
    |                       |   Send Tournament      |  Tournament has +-----------------------------+
    |                       |   Results              |  ended              |
*13 | <--------------------------------------------+ |                     |
    |                       |                        |                     |
    | Received Confirmation |                        |                     |
*14 | +--------------------------------------------> |                     |
    |                       |                        |                     |
    |                       |  Report Tournament     |                     |
    |                       |  Results               |                     |
    |                       | <--------------------+ |                     |
    |                       |                        |                     |
    |                       |                        |                     |
    |                       |                        |                     |
    +                       +                        +                     +
```
  
## Protocol Description
In this protocol the Fish.com Servers column represents the remote communication layer between our internal 
Tournament Manager and the remote Players. All interactions that cross this layer will be translated from 
our internal class representations into JSON which can be transmitted over TCP. 

Local components like the Tournament Manager and Referee will contact a ProxyPlayer implementation that
will handle this translation from internal to JSON representations. See below for specific JSON representations
for each message type, where the *_ in the above diagram corresponds to the JSON format below.
Additionally the external Players will communicate with a Proxy Tournament Manager and Proxy Referee that will
convert JSON into our internal representation.  

Our Proxy components will be used to handel any timeout events in communication between external Players, and 
the Tournament Manager and Referee. 

### Signing up for the tournament
```
*1 { "type": "signup_request", "value": String } 
- A unique identifier to use as a Player's username.
*2 { "type": "signup_confirmation", "value": Boolean }
- True if the Player has been entered into the tournament, False if the Player has been placed on a waitlist. 
```

### Starting the tournament
```
*3 {"type":  "tournament_start", "value": True }
- Broadcast that the tournament has started to all users
*4 {"type": "tournament_ready", "value": Boolean }
- True if the Player is ready to start the tournament, False if the Player is not ready (will be removed from tournament)
```

### Playing the game
```
*5 { "type": "player_assign_color", "value": Color }
- A String representing the Player's color for this game, this message is also used to indicate to Players that a new game is starting.
*6 { "type": "player_request_placement", "value": State }
- Referee is requesting player to place a penguin on the given state
*7 { "type": "player_respond_placement", "value": Position }
- Player responds with the position to place their penguin 
*8 { "type": "broadcast_state", "value": State }
- Broadcast that the game is starting. This message format will be used to broadcast future states when necessary.
*9 { "type": "player_request_move", "value": True }
- Referee is requesting a move from the Player
*10 { "type": "player_respond_move", "value": Action }
- Player responds with their next move.
*11 { "type": "broadcast_action", "value": Action }
- Referee broadcasts each action that is taken in the game
*12 { "type": "broadcast_game_over", "value": GameResult }
```

### Ending the tournament
```
*13 { "type": "tournament_end", "value": Boolean }
- True if the Player won, False if they lost. This message is sent to all active players (those who have not failed or cheated).
*14 { "type": "tournament_end_response", "value": Boolean }
- True if Player receives and accepts the message. If winning player fails to respond, they become a loser when results are 
reported to the server. 
```

### Data Definitions
```
An Action is one of:
- [Position, Position]
- "Skip"
and represents an action taken by the Player during the game

A GameResult is a JSON object as follows:
{
  "winners": [List-of String],
  "losers": [List-of String].
  "kicked_players": [List-of String],
  "state": State
}
and represents the end result of one game of Fish.

A Position is a tuple as follows:
[ Natural, Natural ]
and represents a position on the board with row, and column respectively.

A State is a JSON object as follows:
{
  "board": [List-of [List-of Natural]]
  "players": [List-of Player]
}
and represents a game state, where board is a nested array of natural numnbers
which represent the fish count on each tile.

A Player is a JSON object as follows:
{
  "name": String,
  "places": [List-of Position],
  "color": Color
}
and represents a player of the Fish game.

A Color is one of "red", "white", "brown", or "black".
```

### Sign-up
- Players send sign-up requests to the Fish.com Servers
  - recieve a message confirming they are in a tournament or on a waitlist
- When there are enough Players to run a tournament the server will ask the Tournament Manager to start a tournament
  - The server will send the Tournament Manager a list of Players in ascending order by age in this tournament

### Tournament
- The Tournament Manager communicates the start of the tournament to all Players and Observers. 
- The Tournament Manager listens for Player responses that they are ready to start
  - unresponsive Players will be kicked from the tournament. 
- The Tournament Manager will run the tournament in rounds untill winners are determined.
  - divide Players into games in ascending order of age
  - creates a Referee and has it run all the games in this round
  - Referee is given the list of Players, and board dimensions and asked to run a game of fish.
  - Players who lost will be eliminated from future rounds
- When the tournament is over the Tournament Manager will inform Players if they have won or lost. 
  - unresponsive winners will become losers
- Finally the Tournament Manager will report the results to the Fish.com Servers.

### Game
- The Referee assigns Colors to all of the Players in the game.
- The Referee then requests penguin placements from the Players in turn order untill all penguins are placed.
- The Players are required to respond with valid coordinates to each placement request.
  - Players who fail to respond or respond with invalid coordinates will be kicked
- The Referee broadcasts the starting game state to all Players and any game observers.
- The Referee runs the game by requesting moves from Players in turn order until the game is over.
- The Players are required to respond with a valid move to each move request.
  - Players who fail to respond or respond with an invalid move are kicked.
- After a sucessful action has been performed the Referee broadcasts this action to all Players and observers.
- If any Players are kicked from the game the Referee will remove them and broadcast the new state to all Players and observers.
- When the game is over The Referee informs all Players and observers with the GameResult
- Finally the Referee will return the GameResult to the Tournament Manager