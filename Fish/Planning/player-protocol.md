# Player Protocol
The protocol for the player interface.

## For Player Turns
The referee will ask the player to choose their next move on the board with `choose_next_move(moves)` where moves is a dictionary of their possible actions on the board to their resulting GameTrees.

The player will return an Action. 

The referee will check the validity of the returned Action.
- If it is valid it will execute the action on the current GameTree. 
- Otherwise it will kick the player by removing its penguins from the board. No points are awarded to the player. 

The referee will call `move_penguin(from_posn, to_posn, fish)` according to the Action.
- The player is allowed to add the given fish to their score. The referee will check that the player added to their score correctly. 

## Other Functions
The referee may call getter methods on the player.   
