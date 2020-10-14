# Fish
Python3 project for Fish dot com

CS 4500 Project by Jennifer Der and Timothy Haas

## Project Directory

```
.                           # Fish Project Directory
├── Common/                 # Holds all files for Fish Program (includes data representation, game logic, and unit tests)
│   ├── Test/               # Directory of all Python unit tests
│   ├── Board.py            # Representation of Fish game board
│   ├── Color.py            # Color Enum
│   ├── Player.py           # Data representation of player
│   ├── State.py            # Data representation of game state
│   ├── Constants.py        # Constants for rendering and game constants
│   ├── Tile.py             # Representation of hexagonal tile on board
│   └── Util.py             # All utility functions used throughout Project
├── Planning/               # Memos for Fish game planning   
│   ├── game-state.md       # Design description for data representation of Game States and the external interface
│   ├── games.md            # Design data representation for full games
│   ├── milestones.pdf      # Week 1 memo task Fish milestones
│   ├── self-1.md           # Week 1 self evaluation
│   ├── self-2.md           # Week 2 self evaluation
│   └── system.pdf          # Week 1 memo task for Fish software components
├── xtest                   # Test script 
└── README.md               # This README file
```

## Software Components
![Class Diagram](https://i.imgur.com/nTRzWTd.png)
### Board
The Game Board has a two-dimensional array of Tile objects, and calls functions in the Tile class such as `create_hole`, and `set_fish` during Board construction.
### Hexagonal Board Coordinate System
```
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
- Positions on the Board are represented throughout the project by a (row, col) tuple.

### Tile
Data representation of a hexagonal tile. A Tile object has a north, south, northeast, northwest, southeast, southwest direction. 

### State
Keeps track of the Board and the Players in the current state. State also keeps track of which Player's turn it is. The list of Players that State keeps is an ordered list from youngest to oldest.

### Player
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


## Testing
Run all unit tests for Fish:
```
$ cd Fish/
$ ./xtest
```
Run individual unit test file for Fish:
```
$ cd Fish/Common/
$ python3 -m unittest Test/<name_of_test_file.py>
```
Run an individual unit test:
```
$ cd Fish/Common/
$ python3 -m unittest -v Test.<name_of_test_file>.<TestClass>.<name_of_test_function>
# example:
$ python3 -m unittest -v Test.board_test.BoardTestCase.test_create_board_with_holes
```

