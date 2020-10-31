## Self-Evaluation Form for Milestone 5

Under each of the following elements below, indicate below where your
TAs can find:

- the data definition, including interpretation, of penguin placements for setups 
- [Function to place penguins at setup](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Player/strategy.py#L18-L44)
- [Player class in README includes data definition for penguins](https://github.ccs.neu.edu/CS4500-F20/anton/tree/d3ea2ddb3d469da3440af2836670edce4a273973/Fish#software-components) 
- [Example of adding penguins](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Common/Player.py#L39-L46)

- the data definition, including interpretation, of penguin movements for turns
- [Function to move penguin on turns](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Player/strategy.py#L46-L66)
- [Interpretation for Action](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Common/Action.py#L1-L4) 
- [Interpretation and Constructor for Move](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Common/Move.py#L3-L12)
- [Interpretation for Pass](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Common/Pass.py#L2-L5)

- the unit tests for the penguin placement strategy 
- [place penguin test](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Other/strategy_test.py#L78-L98)

- the unit tests for the penguin movement strategy; 
  given that the exploration depth is a parameter `N`, there should be at least two unit tests for different depths 
- [penguin movement test](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Other/strategy_test.py#L101-L135)
  
- any game-tree functionality you had to add to create the `xtest` test harness:
- We did not add anything to game_tree but these functions we used in xtree
- [xtree functions](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/5/xtree#L48-L96)
- [We found a bug in Board that we corrected](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Common/Board.py#L135-L152)
    - Our reachable positions was hopping over other penguins and was returning tiles beyond those positions.
    - [This is the test we added](https://github.ccs.neu.edu/CS4500-F20/anton/blob/d3ea2ddb3d469da3440af2836670edce4a273973/Fish/Other/board_test.py#L205-L207)
**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "d3ea2ddb3d469da3440af2836670edce4a273973".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/anton/tree/d3ea2ddb3d469da3440af2836670edce4a273973/Fish>

