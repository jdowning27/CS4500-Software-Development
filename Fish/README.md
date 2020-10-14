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
![Class Diagram](https://i.imgur.com/RlwPXWY.png)
### Board
The Game Board has a two-dimensional array of Tile objects, and calls functions in the Tile class such as `create_hole`, and `set_fish` during Board construction.

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

