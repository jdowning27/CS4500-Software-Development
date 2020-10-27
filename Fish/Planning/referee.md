# Referee
The data representation for Referee and design for its interface

## Data representation
A Referee keeps track of:
- The current GameTree
    - This includes the functionality to find out whose turn it is currently
- Set of Player
- Set of Players who have been kicked out of the game 
- History of Player's moves or actions
    - This represents the whole history of the game

## Interface (API)
```
"""
Start the game. Initializes the game board, the game state, and the resulting game tree with the parameters.

1. Takes care of what kind of Board to make (does it have holes, number of fish, etc), and makes sure that the board is big enough for the number of players and their penguins

2. Calls on Players to place their penguins

The resulting GameTree is ready to play.

[Listof Player] -> GameTree
"""
def initialize_game(players):
    pass


"""
Check that the given action is valid in the current state of the game tree. If it is valid, return the next game tree with the action applied, otherwise False

Action -> [Maybe GameTree]
"""
def check_move_validity(Action):
    pass

"""
Utility method to see if the game has ended.

void -> Boolean
"""
def has_game_ended():
    pass

"""
Get the current state of the game to inform game observers of on-going actions. Returns a JSON translation of the current state, which is read-only.

void -> JSON Object
"""
def get_current_state():
    pass

"""
Get scores of players.

void -> {Player: int}
"""
def get_curr_scores():
    pass

"""
Get the winner of the game. If the game has not ended and there is no winner, return False.

void -> [Maybe Player]
"""
def get_winner():
    pass

"""
Get the game history. The tournament manager may use this in its own tournament statistics. Returns a list of Player to Action mappings.

void -> [Listof (Player, Action)]
"""
def get_history():
    pass
```