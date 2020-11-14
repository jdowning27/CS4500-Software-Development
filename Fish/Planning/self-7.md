## Self-Evaluation Form for Milestone 7

Please respond to the following items with

1. the item in your `todo` file that addresses the points below.
    It is possible that you had "perfect" data definitions/interpretations
    (purpose statement, unit tests, etc) and/or responded to feedback in a 
    timely manner. In that case, explain why you didn't have to add this to
    your `todo` list.

2. a link to a git commit (or set of commits) and/or git diffs the resolve
   bugs/implement rewrites: 

These questions are taken from the rubric and represent some of the most
critical elements of the project, though by no means all of them.

(No, not even your sw arch. delivers perfect code.)

### Board

- a data definition and an interpretation for the game _board_

  - Todo item:  
    - [No interpretation of the data/type definition for a board/coordinates representation.](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/7/todo.md#L17)

  - Fixed:  
    - [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/fbb418207443e0c05314aa68db7c69bc67fce761#diff-92f6d081922bb0aae4366590406c99a6R12)
    - [Added coordinate system interpretation to README](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/af3702f2047a632712c96a1c22ff57932934aa74#diff-f4923aab63564278027a266fe91df7a4R34-R49)

- a purpose statement for the "reachable tiles" functionality on the board representation

  - Todo item:  
    - [Reachable-tiles purpose statement does not specify positions are reachable via straight lines](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/7/todo.md#L18)

  - Fixed:  
    - [Added to purpose statement of reachable positions function](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/8b005b54ed9ea5539d9d7adcc8c62659bd7472b7)
    - [Added explanation and examples in README](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/af3702f2047a632712c96a1c22ff57932934aa74#diff-f4923aab63564278027a266fe91df7a4R48)


- two unit tests for the "reachable tiles" functionality

    Our code base correctly addressed these tests from the beginning. The 
test can be found here:
  - [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/Fish/Other/board_test.py#L144-L152)


### Game States 


- a data definition and an interpretation for the game _state_

  - Todo item:  
    - [Insufficient interpretation of the game state](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/7/todo.md#L13)

  - Fixed:  
    - [improved state interpretation](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/b57f7bc2e09f50b454cab4d8d212dce4b7f88c48#diff-3c0c742881289081d1c3cfb361c6da0eR10-R13)

- a purpose statement for the "take turn" functionality on states

  Our code originally included a good purpose statement for taking turns.
It can be found here:  
  - [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/Fish/Common/state.py#L78-L80
)

- two unit tests for the "take turn" functionality 
  
  We had two tests for this and added to existing tests after receiving 
feedback that we were not testing advancing to the next player.

  - [Tests](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/6b14b712069cae255394d617a8207a91d8599f26#diff-a8e5da7c984b37a424912da551eef7f5R120-R137)


### Trees and Strategies


- a data definition including an interpretation for _tree_ that represent entire games

  - Todo items:   
    - [Data definition/interpretation of the game tree doesn't mention how "skip" transitions are dealt with](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/7/todo.md#L10)

    - [it is unclear if the game tree node can represent all three kinds of nodes](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/7/todo.md#L14)

  - Fixed:  
    - [Skip Interpretation](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/a9942bc6d71697d13e4f55c9e2dcbda5f80dd57e#diff-a2b85550c39cc14472cf741196ccb390)
    - [Game Interface Representation](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/08d4300f27781efac24b411041b421aff1218067#diff-2d8e341e1a13a7b67eb38f98c777b250)
    - [GameSetup Representation](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/08d4300f27781efac24b411041b421aff1218067#diff-5115f5114cc9ed544f40383593fd68f0)
    - [GameEnded Representation](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/08d4300f27781efac24b411041b421aff1218067#diff-c77c569101b9e5a0ce0462b0cd966880)

- a purpose statement for the "maximin strategy" functionality on trees
  
  Our code originally included a signature for the "maximin strategy".
It can be found here:  
  - [Purpose Statement](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/Fish/Player/strategy.py#L52-L59)

- two unit tests for the "maximin" functionality 

  Our code originally included unit tests for maximin. They can be found 
here:  
  - [Tests](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/Fish/Other/strategy_test.py#L102-L136)


### General Issues

Point to at least two of the following three points of remediation: 


- the replacement of `null` for the representation of holes with an actual representation 

  Our code did not use `null` to represent holes on the board. The tile 
class is able to represent both holes and tiles. 

- one name refactoring that replaces a misleading name with a self-explanatory name

  Our PlayerData class and AI Player class prigionally had the same names. 
We changed the names to they could be more easily identifiable. 

  - [Name Change](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/1a33e0b3a339c5f03b8ac1cda26bc1aec26ef16a)

- a "debugging session" starting from a failed integration test:
  - the failed integration test
  - its translation into a unit test (or several unit tests)
  - its fix
  - bonus: deriving additional unit tests from the initial ones 

  We did not experience any "debugging session"s when creating integration 
tests. Our implementation was able to successfully run the integration 
tests created by us and other students. This is an example of a unit test that broke our code and resulted in a "debugging session". 

  Our best gain function was not returning answers when attempting to find 
the next best move. Additionally it was returning the same result even 
when the depth was changed. 
  - [Failing Strategy Code](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/7c9f78f0c027e261baee2774e7a0cc93471594f3/Fish/Player/strategy.py#L38-L97)
  - [Reworked Strategy](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e135224fd88549b4f2030ce64660eb4e59d9ed64/Fish/Player/strategy.py#L38-L110)  
  - [Exposing Test](https://github.ccs.neu.edu/CS4500-F20/detroit/blob/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/Fish/Other/strategy_test.py#L117-L122)

### Bonus

Explain your favorite "debt removal" action via a paragraph with
supporting evidence (i.e. citations to git commit links, todo, `bug.md`
and/or `reworked.md`).

Our favorite debt removal action was fixing the lazy generation of 
our GameTree. Instead of re-creating the children of the game tree 
every time, we would look into a dictionary of child branches to 
check if the child existed before creating a new one. This change 
also led us to rework our player's protocol with the referee. This 
change enabled the player to traverse and generate their own tree 
instead of the referee having to pass a tree to the player. These 
two changes combined lead to much faster code. Before a game that ran an entire game to completion would take about 20 seconds. Now that same test runs in under one second. This change also added security to our implementation. Now the player and referee no longer share a reference to the tree object, which prevents the player from manipulating the game. 

Todo items:
- [Tree Generation Todo](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/7/todo.md#L44-L47)

- [Protocol Todo](https://github.ccs.neu.edu/CS4500-F20/detroit/blame/e61ae3e8d6548c64ca3d2166ce77b0b2d3673ccd/7/todo.md#L54-L58)

Rework:
- [Game Tree Rework](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/04bf927305b5586b28d6428f528e785f826ce37d)

- [Protocol Rework](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380)
