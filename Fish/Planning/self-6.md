## Self-Evaluation Form for Milestone 6

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

The implementation of the "steady state" phase of a board game
typically calls for several different pieces: playing a *complete
game*, the *start up* phase, playing one *round* of the game, playing a *turn*, 
each with different demands. The design recipe from the prerequisite courses call
for at least three pieces of functionality implemented as separate
functions or methods:

- [the functionality for "place all penguins"](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L59-L90)

- [a unit test for the "place all penguins" funtionality](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Other/referee_test.py#L27-L39)

- [the "loop till final game state" function](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L31-L56)

- [this function must initialize the game tree for the players that survived the start-up phase](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L89)
  - note: this is the line where GameTree is initialized


- [a unit test for the "loop till final game state"  function](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Other/referee_test.py#L54-L63)


- [the "one-round loop" function](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L40-L54)
  - note: we did not split this out into a separate function, but this is where the functionality is

- a unit test for the "one-round loop" function
  - because this is not a separate function, we do not have a unit test for one round


- [the "one-turn" per player function](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L41)
  - do not have function for one player's turn, linked above is where the current player chooses one move, then
  - [goes to next player's turn](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L54)


- [a unit test for the "one-turn per player" function with a well-behaved player](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Other/referee_test.py#L54-L56)
  - note: we are missing a one-turn per player function, linked above is an entire game being played with no illegal moves


- [a unit test for the "one-turn" function with a cheating player](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Other/referee_test.py#L58-L63)
  - note: linked above is a game where all moves that players return are mocked as invalid


- a unit test for the "one-turn" function with an failing player 
  - missing test because we do not have other ways right now for a player to fail (ie. no timeout)


- [for documenting which abnormal conditions the referee addresses](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L13) 


- the place where the referee re-initializes the game tree when a player is kicked out for cheating and/or failing 
  - [line where current game is replaced](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Admin/referee.py#L47)
  - [where the new game tree is created (in a helper function in GameTree which is called by the Referee)](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish/Common/game_tree.py#L129-L136)





**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/anton/tree/d2900e7790ea5e4ff86f1c342bdd6fd198f98ba4/Fish>

