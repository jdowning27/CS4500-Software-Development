# Fish
Python3 project for Fish dot com

CS 4500 Project by Jennifer Der and Timothy Haas

## Project Directory

```
.                           # Fish Project Directory
├── Admin/                  # Directory for files relating to game management
│   ├── referee.py          # Data representation of a game referee
│   └── manager_interface.py # Data representation for a tournament manager
├── Common/                 # Holds all files for Fish Program (includes data representation, game logic, and unit tests)
│   ├── action.py           # Interface for a game action
│   ├── board.py            # Representation of Fish game board
│   ├── color.py            # Color Enum
│   ├── constants.py        # Constants for rendering and game constants
│   ├── game_tree.py        # Representation of the a Fish game
│   ├── move.py             # Representation of a penguin's move, implements Action
│   ├── skip.py             # Representation of no move possible in game, implements Action
│   ├── player_interface.py # Representation of a player interface, to be used by other components
│   ├── player.py           # Data representation of player
│   ├── state.py            # Data representation of game state
│   ├── tile.py             # Representation of hexagonal tile on board
│   └── util.py             # All utility functions used throughout Project
├── Other/                  # Directory of all Python unit tests
├── Planning/               # Memos for Fish game planning   
│   ├── game-state.md       # Design description for data representation of Game States and the external interface
│   ├── player-protocol.md  # Design description for how components will interact with the player interface
│   ├── referee.md          # Design description for Referee
│   ├── games.md            # Design data representation for full games
│   ├── manager-protocol.md # Design description for how the manager interacts with other components
│   ├── milestones.pdf      # Week 1 memo task Fish milestones
│   ├── self-1.md           # Week 1 self evaluation
│   ├── self-2.md           # Week 2 self evaluation
│   ├── self-3.md           # Week 3 self evaluation
│   ├── self-4.md           # Week 4 self evaluation
│   └── system.pdf          # Week 1 memo task for Fish software components
├── Player/                 # Files relating to Players 
│   ├── player.py           # Data representation of an external player
│   └── strategy.py         # Strategies for players to place penguins and minimax optimization for actions
├── xtest                   # Test script 
└── README.md               # This README file
```

## Software Components
![Class Diagram](https://i.imgur.com/wMdeS7o.png)

### External Player
The external player implements the Player Interface that is outlined [here](https://github.ccs.neu.edu/CS4500-F20/anton/blob/master/Fish/Common/player_interface.py). AI, Remote, and House players are able to implement this interfaced in order to participate in Fish game tournaments

### Referee
The referee is in charge of managing the game. There is one Referee for each game within a tournament. The Referee communicates with the External Players, the internal game system, as well as reporting game outcomes to both the tournament manager, observers, and external players.


### Strategy
Currently, only one strategy class has been implemented. Players may use this class when playing the game. 
This gameplay functionality is implemented as a class so that players may choose how to strategize for the game when they are initialized for this specific game/round.

### GameTree
The Game Tree consists of a current state and a dictionary pointing to child game trees, where the key is the move or action that results in the value tree.
```
# Example usage for how to create N layers of the full Game Tree
# Given that an instance of a game state exists...
tree = GameTree(state)
tree.create_child_trees() # will create the first layer of child trees for this tree
# Create child trees for the children of the tree above...
children = GameTree.apply_to_children(tree, GameTree.create_child_trees)
# Repeat process N times, for each of the children created...
grandchildren = []
for child in children:
    grandchildren.append(GameTree.apply_to_children(child, GameTree.create_child_trees)) # creates a nested list of the grandchildren trees
```
### Board
The Game Board has a two-dimensional array of Tile objects, and represents a hexagonal game board for Fish. The coordinate system is described below.
### Hexagonal Board Coordinate System
```
# Example of a 4 row, 3 column board
  _____         _____         _____
 /     \       /     \       /     \
/ 0, 0  \_____/  0, 1 \_____/  0, 2 \_____
\       /     \       /     \       /     \
 \_____/ 1, 0  \_____/  1, 1 \_____/  1, 2 \
 /     \       /     \       /     \       /
/ 2, 0  \_____/  2, 1 \_____/  2, 2 \_____/
\       /     \       /     \       /     \
 \_____/ 3, 0  \_____/  3, 1 \_____/  3, 2 \
       \       /     \       /     \       /
        \_____/       \_____/       \_____/
```
- Reachable positions on the board from one tile are positions that can be reached by a straight line over borders (not corners) of the hexagon. If a hole is reached (Tile with no fish), the path stops. Positions are not reachable through 'jumping' over holes on the board.
  - Example: In the above board, (2, 0) and (3, 1) are reachable from **(0, 0)** but (0, 1) and (3, 0) are **not**.
- Positions on the Board are represented throughout the project by a (row, col) tuple.

### Tile
Data representation of a hexagonal tile. A hexagonal tile has a north, south, northeast, northwest, southeast, southwest direction and methods to get the coordinates to a Maybe Tile in each direction. 

### State
Keeps track of the Board and the Players in the current state. State also keeps track of which Player's turn it is. The list of Players that State keeps is an ordered list from youngest to oldest.

### Internal Player
The internal data representation of a Player. A Player has access to their penguins, where a penguin is represented by a (row, col) tuple which is their location on the Board.

### Examples of how to create boards, and render

Create a board that has holes in specific places and is set up with a minimum number of 1-fish tiles. 
![Fish Board with Holes](https://i.imgur.com/PCWOPuJ.png)
```
board = Board(4, 3)
holes = [(0, 0), (0, 1), (3, 2)] 
min_tiles = 3
board.create_board_with_holes(holes, min_tiles)
```

Create a board that has the same number of fish on every tile and has no holes
![Fish Board No Holes](https://i.imgur.com/q8TYTyn.png)
```
board = Board(4, 3)
board.create_board_without_holes(4)
```

Also, there is an option to create an intermediate game board using a two-dimensional array
```
my_board = [
            [1,     2,      3,      0],
                [4,     0,      0,      5],
            [1,     1,      0,      1]
]
board = Board(4, 3)
board.create_board_from_json(my_board)
```

Other functionality
```
# Get list of all reachable positions from positions
board = Board(4, 3)
board.create_board_with_holes([(0,0)], 1)
board.get_all_reachable_posn(1, 0) 
# returns => [(3, 0), (0, 1), (2, 0), (2, 1), (3, 1)])

# Remove a tile from a board
board.remove_tile(0, 0)

# Render all tiles graphically
board.draw_board()
```

## Building
Run make inside the `Fish` directory to install the package before running tests:
```
elkhart/Fish/$ make
```


## Testing
Run all unit tests for Fish:
```
$ cd Fish/
$ ./xtest
```
Run individual unit test file for Fish:
```
$ python3 -m unittest Other/<name_of_test_file.py>
```
Run an individual unit test:
```
$ python3 -m unittest -v Other.<name_of_test_file>.<TestClass>.<name_of_test_function>
# example:
$ python3 -m unittest -v Other.board_test.BoardTestCase.test_create_board_with_holes
```

