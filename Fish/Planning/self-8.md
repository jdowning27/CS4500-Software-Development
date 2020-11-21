## Self-Evaluation Form for Milestone 8

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

1. did you organize the main function/method for the manager around
the 3 parts of its specifications --- point to the main function
- [Purpose statement and signature for the main function (in interface)](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager_interface.py#L13-L28)
- [`run_tournament` function](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager.py#L41-L53)

2. did you factor out a function/method for informing players about
the beginning and the end of the tournament? Does this function catch
players that fail to communicate? --- point to the respective pieces
- [Communicating the start of the tournament](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager.py#L169-L183)
- [Communicating the end of the tournament](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager.py#L186-L203)
- [Both functions catch players who fail to communicate (throw an error) using the safe call method](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager.py#L213-L224)
  - Currently, we do not have a way to handle player timeouts, and only handle when the player raises an exception or returns a bad response.

3. did you factor out the main loop for running the (possibly 10s of
thousands of) games until the tournament is over? --- point to this
function.
- [`run_round` function runs a single round](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager.py#L84-L104)
- [The functionality for the main loop is here, which calls `run_round` until the tournament is over](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager.py#L84-L104)
- We did not factor out the main loop for running the tournament from our main run tournament function. `run_round` runs all the games for a single round in the tournament. Since we split out the rest of the functionality for allocating players to games, and broadcasting the tournament started and ended, our run tournament function was relatively small. We felt this simplified our main loop enough so we did not factor it out. It would not make sense to run a tournament without doing the set up steps in [lines 42 and 43](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/4439faea6eaa9bc14350341764b91e404c1ed396/Fish/Admin/manager.py#L42-L43).


**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**


  WARNING: all perma-links must point to your commit "4439faea6eaa9bc14350341764b91e404c1ed396".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/detroit/tree/4439faea6eaa9bc14350341764b91e404c1ed396/Fish>

