# Manager Protocol
The protocol for the tournament manager.

### After the tournament manager has been instantiated:
- Listens for player sign ups through the function `player_signup(player)`
	- Where player is a class that implements PlayerInterface
- Accepts a collection of players sorted by age (where age is determined by when they signed up) from the sign up server
	- Prefers 4 player games, will only create 2 or 3 player games when the number of players is not divisible by 4
	- For example if there are 6 players left it will split them into 2 games of 3
- Listens for observers to sign up
	- When an observer signs up, the tournament manager updates them on on going actions and tournament statistics by sending json through tcp.
- Receives updates about each game from the referee after it has ended
	- Updates include: who won the game, players who have been kicked out for breaking the rules or cheating
	- Removes cheating players from the tournament
- Adds winners into a queue for the next round
	- Repeats this process of starting games and receiving updates for each round until there is a winner for the tournament
	- Players can choose to leave the tournament by calling `leave_tournament(player)`
- If a player remains unresponsive in a game a referee may choose to eject them.
	- The player will be ejected from the tournament. 
- After the tournament has ended
	- Alerts game observers about tournament winner
	- Dispatches tournament payout to third party
