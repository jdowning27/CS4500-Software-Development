# Remote Planning

## Logical Interaction Diagram
```
Players           Fish.com Server         Tournament Manager          Referee
  +                       +                        +                     +
  |    Sign-up Request    |                        |                     |
  | +-------------------> |   Run Tournament w/    |                     |
  | Confirmation/Waitlist |   Players              |                     |
  | <-------------------+ | +--------------------> |                     |
  |                       |                        |                     |
  |                       |    Start Tournament    |                     |
  | <--------------------------------------------+ |                     |
  |    Ready to start     |                        |    Runs N rounds    | <-----------------------+
  | +--------------------------------------------> |    of Games         |                         |
  |                       |                        | +-----------------> |                         |
  |                       |                        |                     |                         |
  |                       |                        |   Assign Colors     |                         |
  | <------------------------------------------------------------------+ |                         |
  |                       |                        |                     |                         |
  |                       |                        |  Request Penguin    |                         |
  |                       |                        |  Placements         |                         |
  | <------------------------------------------------------------------+ |                         |
  |                       |                        |                     |                         |
  | Respond w/ Placement  |                        |                     |                         |
  | Coordinate            |                        |                     |                         |
  | +------------------------------------------------------------------> |                         |
  |                       |                        |                     |                         |
  |                       |                        |  Broadcast Starting |                         |
  |                       |                        |  Game State         |                         |
  | <------------------------------------------------------------------+ |                         |
  |                       |                        |                     |                         |
  |                       |                        |  Request Moves      | <---------------------+ |
  | <------------------------------------------------------------------+ |                       | |
  |                       |                        |                     |                       | |
  |  Respond w/ Moves     |                        |                     |                       | |
  | +------------------------------------------------------------------> |                       | |
  |                       |                        |                     |                       | |
  |                       |                        |  Broadcast Actions  |   If Failing Player   | |
  | <------------------------------------------------------------------+ |   kick them and       | |
  |                       |                        |                     |   Broadcast new State | |
  |                       |                        |                     |                       | |
  |                       |                        |                     |   Repeat until  +-----+ |
  |                       |                        |                     |   Game Over             |
  |                       |                        | Broadcast Game Over |                         |
  | <------------------------------------------------------------------+ |                         |
  |                       |                        |                     |                         |
  |                       |                        |  Return Game Results|                         |
  |                       |                        | <-----------------+ |                         |
  |                       |                        |                     |                         |
  |                       |                        |  Repeat until       |                         |
  |                       |   Send Tournament      |  Tournament has +-----------------------------+
  |                       |   Results              |  ended              |
  | <--------------------------------------------+ |                     |
  |                       |                        |                     |
  | Received Confirmation |                        |                     |
  | +--------------------------------------------> |                     |
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
will handle this translation from internal to JSON representations. 
Additionally the external Players will communicate with a Proxy Tournament Manager and Proxy Referee that will
convert JSON into our internal representation.  

Our Proxy components will be used to handel any timeout events in communication between external Players, and 
the Tournament Manager and Referee. 

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