# Player Protocol
The protocol for the player interface.

## To Setup the Game
The referee will set up the game board and initialize the Game with a given list of Players.

The referee will assign player's colors using `assign_color(player_color)`

The referee will run penguin placement rounds for the players until all players have placed 6 - N number of penguins, where N is the number of players. It does this by calling a method on Player, called `place_penguin(state)`

At this point, the Game is ready to begin.

## For Player Turns
The referee will ask the player to choose their next move on the board with `choose_next_move(moves)` where moves is a dictionary of their possible actions on the board to their resulting GameTrees.

The player will return an Move. 

The referee will check the validity of the returned Move.
- If it is valid it will execute the action on the current GameTree. 
- Otherwise it will kick the player by removing its penguins from the board. No points are awarded to the player. 

The referee will call `move_penguin(from_posn, to_posn, fish)` according to the Move.
- The player is allowed to add the given fish to their score. The referee will check that the player added to their score correctly. 

## After the Game Ends
The Game ends when no player can move a penguin. 
The referee will tell players that the game has ended by calling `game_over(state)` where state is the terminal state of the game. This allows players to look at the final state of the board, see who the winner(s) are and their score(s).

