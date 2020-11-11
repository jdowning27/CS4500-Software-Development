## Must Haves
### Grading Feedback
[X] Data definition/interpretation of the game tree doesn't mention how "skip" transitions are dealt with  
[X] Purpose statement doesn't say what happens when there are no valid moves  
[X] Negative unit test for failed penguin placement, when board is not big enough  
[X] Document behavior in purpose statement  
[X] Insufficient interpretation of the game state, it should be clear what all components of the data definition mean and it is unclear how players are related to penguins  
[X] it is unclear if the game tree node can represent all three kinds of nodes: game-is-over, current-player-is-stuck, and current-player-can-move; only current-player-can-move is obvious  
[X] No info on how many players can play a game  
[X] No unit tests for turn-taking functionality; only tested moving a penguin, the test doesn't show the switch to next player.  
[X] No interpretation of the data/type definition for a tile representation  
[X] No interpretation of the data/type definition for a board/coordinates representation.  
[X] Reachable-tiles purpose statement does not specify positions are reachable via straight lines  

### Integration Tests
[X] Fix JSON integration tests  
- Milestone 6: Fish values should be [0, 5]
- Milestone 5: Made changes to State, Players need 6 - N penguins
- Milestone 4: Need appropriate number of Players
- All: Needed to update PlayerData constructor call with contract checking for Color


## Nice to Haves
### Code base
[X] Contract checking  
- [X] Check instances of players in Referee as well as in State (for internal players)
- including: no players with same color, the class type

[X] Rename all files, stick to lowercase_underscore.py naming convention  

[] Update documentation  
- [] Function signatures
- [] Revisit naming of some functions (check_move_validity, move_penguin)
- [] Update player-protocol.md doc
    - Player is not given a list of moves to decide on next move, it is given a GameTree (or State depending on rework of protocol)

[] Privatizing fields throughout code base
- [] Priotize State
- [] Privatize fields in GameTree, and implement appropriate getters, `GameTree.get_winners` should not return winners  

### Game
[] Rework how next action in GameTree is applied
- Do not regenerate a new GameTree when given an action, search through children first for the action and return the resulting GameTree if found. Only after action is not found in children, generate the resulting GameTree with a new state.
- Generate a GameEnded when no player can make a move during tree generation
- [] Fix the maximal gain strategy to fit the new GameTree implementation

[] Game result to also return the set of kicked players from the game

### Player
[X] Renaming Player classes: Need to have an external Player class and a State Player (internal data representation)
### External Player Protocol
[] Give the Player a State when asking for the next move instead of a Tree  
[] Referee communicates changes in the game to players  
- Notify players of other players actions on the board and when others are kicked out of the game
- [] Remove move_penguin function
    - Dependent on protocol rework: add a function that lets the player know the new state of the game after they have made their move 


### Referee
[] Extract constants out of Referee
- [] List of colors
- [] Function that returns the maximum number of penguins
[] Add helper functions for playing the game
- [] One function for taking one turn, plus unit tests
[] Add functionality for external players time out
- [] Also add to list of ways a player can be kicked in docs
### Board
[] Move tile coordinate system to Board  
- Currently, Tiles know their position on board, this should be taken out completely and only exist in Board  

[] Implement a Tile Interface to have separate classes for an active Tile versus a Hole  
[] Generate a Board using a Board Config  


### Other
[] Move JSON printing and parsing to an external utilities class or file  
[] Using Python deepcopy over written copy functions  

