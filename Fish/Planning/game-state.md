# Game State
In order for players and referees to manipulate game states, they will need a data representation of the board at any given time. This data representation may include:
- The State of the Board 
    - including which Tiles are reachable from their Penguins
    - number of Fish on each Tile
    - which Tiles are holes in the board
- List of Players
    - list of Penguins (including their current positions)
    - score of each Player
- Which Player's turn it is

# External Interface
The external interface is what Players and Referees will use to manipulate game states. These two roles will be separated into two different interfaces as follows:

### The Player
- method to move a Penguin per turn
- method to see scores
- method to see all possible reachable positions for each Penguin
- method to see state of the Board (above data representation)
- know when their turn is

### The Referee
- method to see the state of the Board (above data representation)
- method to see all Player's scores
- method to determine the exact layout of the board (ie. make holes in the board) after being told the row x col dimensions
- knows whose turn it is, and whose turn is next
    - tells Players when it is their turn
    - ability to start each round
- method to assign each Player a Penguin color
- ability to run Penguin placement rounds for each Player
- ability to remove Players and their Penguins that fail or cheat
- reports the outcome of the game and the failing/cheating Players at the end of the game
- informs game-observers of the current state of the game


