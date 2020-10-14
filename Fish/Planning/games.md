# Game

## Data Representation
Data representation for games where both players and referees have ability to plan ahead and check validity of actions.
The Game includes:
- current game State
- Whose turn it is

The interactions between Referee and Game:
- Referee tells Game whose turn it is
- Referee can check validity of moves

The interactions between Player and Game:
- Get current game State
- Plan ahead by getting possible future States

## External Interface
In a game players and referees will need to plan ahead and check rules. These are methods they are able to use to do so given any game state. Assume starting state is when all players have placed penguins.

Players and Referees both have access to this interface.

```
'''
Get current game state
Input: void
Output: State
'''
def get_current_game_state():


'''
Get all possible future game states for given player from given game state
Input: Player, State
Output: List of States
'''
def get_future_states(player, state):


'''
Get reachable positions for player on given state
Input: Player, State
Output: List of (from(tuple), to(tuple))
'''
def get_reachable_posn(player, state):


'''
Is the given move valid for this player? 
Returns the next game state if the move is valid else false
Input: Player, State, from(tuple), to(tuple)
Output: maybe State
'''
def check_move_ahead(player, state, from, to):
```
