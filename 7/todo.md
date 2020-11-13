## Must Haves
### Grading Feedback

#### Unit Tests
- [X] Negative unit test for failed penguin placement, when board is not big enough
- [X] No unit tests for turn-taking functionality; only tested moving a penguin, the test doesn't show the switch to next player.  
- [ ] Cover different abnormal player conditions such as timeout, an exception. 

#### Documentation and Interpretation
- [X] Data definition/interpretation of the game tree doesn't mention how "skip" transitions are dealt with  
- [X] Purpose statement doesn't say what happens when there are no valid moves    
- [X] Document behavior in purpose statement (strategy) 
- [X] Insufficient interpretation of the game state, it should be clear what all components of the data definition mean and it is unclear how players are related to penguins  
- [X] it is unclear if the game tree node can represent all three kinds of nodes: game-is-over, current-player-is-stuck, and current-player-can-move; only current-player-can-move is obvious  
- [X] No info on how many players can play a game  
- [X] No interpretation of the data/type definition for a tile representation  
- [X] No interpretation of the data/type definition for a board/coordinates representation.  
- [X] Reachable-tiles purpose statement does not specify positions are reachable via straight lines  

### Integration Tests
- [X] Fix JSON integration tests  
  - [X] Milestone 6: Fish values should be [0, 5]
  - [X] Milestone 5: Made changes to State, Players need 6 - N penguins
  - [X] Milestone 4: Need appropriate number of Players
  - [X] All: Needed to update PlayerData constructor call with contract checking for Color


## Nice to Haves
### Code base
- [X] Contract checking  
  - [X] Check instances of players in Referee as well as in State (for internal players)
  - [X] including: no players with same color, the class type

- [X] Rename all files, stick to lowercase_underscore.py naming convention  

- [ ] Update documentation  
  - [ ] Function signatures

- [ ] Privatizing fields throughout code base
  - [ ] Priotize State
  - [ ] Privatize fields in GameTree, and implement appropriate getters, `GameTree.get_winners` should not return winners  

### Game
- [X] Rework how next action in GameTree is applied
  - [X] Do not regenerate a new GameTree when given an action, search through children first for the action and return the resulting GameTree if found. Only after action is not found in children, generate the resulting GameTree with a new state.
  - [X] Generate a GameEnded when no player can make a move during tree generation
  - [X] Fix the maximal gain strategy to fit the new GameTree implementation

- [X] Game result to also return the set of kicked players from the game

### Player
- [X] Renaming Player classes: Need to have an external Player class and a State Player (internal data representation)
### External Player Protocol
- [X] Do not pass the Player a GameTree when asking for next move
- [X] Referee communicates changes in the game to players  
  - [X] Notify players of other players actions on the board and when others are kicked out of the game
  - [X] Remove move_penguin function
  - [X] Add a function that lets the player know the new state of the game after they have made their move 


### Referee
- [X] Extract constants out of Referee
  - [X] List of colors
  - [X] Function that returns the maximum number of penguins  
  
- [X] Add helper functions for playing the game
  - [X] One function to initialize, one to run the game, and one to return the end result  
  
- [ ] Add functionality for dealing with abnormal players by wrapping player calls in a protected function
  - [ ] deal with external players timing out
  - [ ] deal with players throwing exceptions
  - [ ] Also add to list of ways a player can be kicked in docs
  
- [ ] Remove unused history field

### Board
- [ ] Move tile coordinate system to Board  
  - Currently, Tiles know their position on board, this should be taken out completely and only exist in Board  

- [ ] Implement a Tile Interface to have separate classes for an active Tile versus a Hole  
- [ ] Generate a Board using a Board Config  


### Other
- [ ] Move JSON printing and parsing to an external utilities class or file  
- [ ] Using Python deepcopy over written copy functions  

