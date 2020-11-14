## Rework

Renamed all files, stick to lowercase_underscore.py naming convention  
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/d99e697c2d16faee4509194d6242650d0b9a238b)

Renamed the Player class used in State to PlayerData
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/1a33e0b3a339c5f03b8ac1cda26bc1aec26ef16a)

Added contract checking to State, redid checking for board and player_data
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/84e71ad12533530d87454f56d4cf23fb1324d9cf)

Added to data interpretation for game tree to mention how a player's turn is skipped.
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/a9942bc6d71697d13e4f55c9e2dcbda5f80dd57e#diff-a2b85550c39cc14472cf741196ccb390)

Added to purpose statement to say what happens when there are no valid moves
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/a9942bc6d71697d13e4f55c9e2dcbda5f80dd57e#diff-8668b6307021688899b1d56141354730)

Updated to State class interpretation to include how players are related to penguins and what each component of the data definition mean
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/b57f7bc2e09f50b454cab4d8d212dce4b7f88c48#diff-3c0c742881289081d1c3cfb361c6da0e)

Added Game interface, as well as GameSetup and GameEnded classes to represent a state where game-is-over, current-player-is-stuck, and current-player-can-move
- [Game Interface](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/08d4300f27781efac24b411041b421aff1218067#diff-2d8e341e1a13a7b67eb38f98c777b250)
- [GameSetup](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/08d4300f27781efac24b411041b421aff1218067#diff-5115f5114cc9ed544f40383593fd68f0)
- [GameEnded](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/08d4300f27781efac24b411041b421aff1218067#diff-c77c569101b9e5a0ce0462b0cd966880)

Added info on how many players can play the game
- [Added to contract checking in State](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/84e71ad12533530d87454f56d4cf23fb1324d9cf#diff-8b59c1ced5e1a2b96a91913cb360a99cR25-R26)
- [Added contract to State class docs](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/4605734b8297b882910557b5e5a2fff6d4c252e8#diff-3c0c742881289081d1c3cfb361c6da0eR21)

Added test for turn taking functionality, show switch to next player after a move
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/6b14b712069cae255394d617a8207a91d8599f26)

Added interpretation for Tile class representation
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/fbb418207443e0c05314aa68db7c69bc67fce761#diff-9ec3aaa69902115ef6ec7c01da1f8a7aR4-R6)

Added interpreation for Board class representation
- [Commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/fbb418207443e0c05314aa68db7c69bc67fce761#diff-92f6d081922bb0aae4366590406c99a6R12)
- [Added coordinate system interpretation to README](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/af3702f2047a632712c96a1c22ff57932934aa74#diff-f4923aab63564278027a266fe91df7a4R34-R49)

Added info about reachable tiles via straight lines
- [Added to purpose statement of reachable positions function](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/8b005b54ed9ea5539d9d7adcc8c62659bd7472b7)
- [Added explanation and examples in README](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/af3702f2047a632712c96a1c22ff57932934aa74#diff-f4923aab63564278027a266fe91df7a4R48)

Rework how next action in GameTree is applied, using lazy generation for GameTree
- [commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/04bf927305b5586b28d6428f528e785f826ce37d)

Extract magic constants out of Referee
- [commit](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/2d2154f0bc9769f2b266ba38f9c35a216010ac24)

Rework Referee game play functions
- [Added helper function to run the game](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR78-R93)
- [Added helper function to run penguin placement](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR196-R215)
- [Game result includes the kicked players](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR185-R194)

Rework Referee to Player Protocol
- Alert Players of each change in the state of the game
    - [After Player is kicked when taking a turn](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR89)
    - [After a Player has made a move](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR92)
- [Alert Players after all penguins have been placed, and before any moves have been made](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR75)
- [Helper functions to alert all active players](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR235-R249)
- [Function to alert Players when game has ended](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-619ed369755f300d8288d31bd5ac934eR175-R182)
- [Remove `move_penguin` and `remove_penguins` function from PlayerInterface](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-4cef33b16438410cec59c5c34c1e7428L36-L54)
    - [Remove from Player](https://github.ccs.neu.edu/CS4500-F20/detroit/commit/5688856ddb01fac068313d9302473ff9da223380?branch=a6af646c1f7850e05d7e2ae19328f0ad739ea12d&diff=split#diff-6288c3ab2dbd1fc8d1576c9da29a569eL47-L57)