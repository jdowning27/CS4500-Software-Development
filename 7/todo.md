## Functionality per data definition
### Code base
[] Privatizing fields throughout code base
    - [] Priotize State
[X] Rename all files, stick to lowercase_underscore.py naming convention
[] Contract checking
    - [] Check instances of players in Referee as well as in State (for internal players)
        - including: no players with same color, the class type
### Game
[] Refactor the Game Interface
    - [] Will need to refactor GameTree (privatizing fields, implementing other methods, etc)
[] Deals with refactoring how we generate a GameTree, need to implement lazy generation
    - [] Refactor the maximal gain strategy to fit the new GameTree implementation
[] Game result to also return the set of kicked players from the game
### Player
[] Renaming Player classes: Need to have an external Player class and a State Player (internal data representation)
### Board
[] Move tile coordinate system to Board
    - Currently, Tiles know their position on board, this should be taken out completely and only exist in Board
[] Implement a Tile Interface to have separate classes for an active Tile versus a Hole
[] Generate a Board using a Board Config
### State
[] Do not pass in a list of penguins to board get all reachable posns function
    - Instead, have method in State to stop exploring the board when you hit another penguin
[] Add method to remove Player with given color, not just the current player
[] Unit test for switching to the next player after one takes a turn
### External Player Protocol
[] Give the Player a State when asking for the next move instead of a list of moves
[] Remove move_penguin function, instead have a function that lets the player know the new state of the game after they have made their move
[] Update player-protocol.md doc
    - Player is not given a list of moves to decide on next move, it is given a GameTree (or State depending on above refactoring)
### Referee
[] Add functionality for external players time out
    - [] Also add to list of ways a player can be kicked in docs
[] Extract constants out of Referee
    - [] List of colors
    - [] Function that returns the maximum number of penguins
[] Refactor functions 
    - [] One function for taking one turn, plus unit tests
### Strategy
[] Negative unit test for failed penguin placement, when board is not big enough
    - [] Document behavior in purpose statement

### Other
[] Update docs
    - [] Function signatures
    - [] Revisit naming of some functions (check_move_validity, move_penguin)
[] Move JSON printing to an external utilities class or file
[] Using Python deepcopy over written copy functions
[] Posn class