## Self-Evaluation Form for Milestone 2

A fundamental guideline of Fundamentals I, II, and OOD is to design
methods and functions systematically, starting with a signature, a
clear purpose statement (possibly illustrated with examples), and
unit tests.

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of tiles, including an interpretation:
[Data Description](https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/README.md)

[Data Interpretation](https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Tile.py#L8)

The description of Tile and its methods is included in the Software Components section of the README

- the data description of boards, include an interpretation:
[Data Description](https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/README.md)

[Data Interpretation](https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Board.py#L16)

The description of Board and its methods is included in the Software Components section of the README

The interpretation is included in the constructor

- the functionality for removing a tile:
  - purpose:
https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Board.py#L147 
  
  - signature:
https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Board.py#L149 

[The README file contains a diagram with the signature for remove_tile](https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/README.md)


  - unit tests:
https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Test/board_test.py#L36 

- the functiinality for reaching other tiles on the board:
  - purpose:
https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Board.py#L65 
  
  - signature:
https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Board.py#L67

[The README file contains a diagram with the signature for get_all_reachable_posn](https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/README.md)
 
  
  - unit tests:
https://github.ccs.neu.edu/CS4500-F20/anton/blob/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish/Common/Test/board_test.py#L92 

This is a test for a 4x3 board with no holes but lines 56-100 have additional test for this function

The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/anton/tree/7a1b43aafc56aa4d8ee37ebe58d62ee4f1e3f100/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.
