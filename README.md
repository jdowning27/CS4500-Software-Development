# Fish.Com
This repo is a project from Northeastern University's CS4500 Software Development.
Contributors to this project are Jennifer Der, Timothy Haas, Joseph Downing, Harrison Gieraltowski.

The goal of this project was to run a tournament of the game Fish for AI players submitted by hackers.
The game of fish is based losely off of the board game [Hey, That's My Fish!](https://www.fantasyflightgames.com/en/products/hey-thats-my-fish/).

Jennifer and Timothy are the origional authors designing the game state and origional player and referee interactions.
Joseph was onboarded by Jennifer after the first programming partner switch. 
Joseph and Jennifer reworked the player and referee interactions and implemented the tournament manager. 
Harrison was onboarded by Joseph after the second and final pair programming partner switch. 
Harrison and Joseph added the Fish/Remote directory containing the adapters and proxies needed to run a game of Fish
with remote players.

## Repository Directory
```
.                           
├── 10/                     # Deliverables for xclient and xserver used run a tournament
├── 3/                      # Deliverable for xboard used for integration testing board
├── 4/                      # Deliverable for xstate used for integration testing state
├── 5/                      # Deliverable for xtree used for integration testing tree
├── 6/                      # Deliverable for xstrategy used for integration testing strategy
├── 7/                      # A list of bugs found and rework done to the code durring the week
├── 8/                      # Deliverable for xref used for integration testing the referee
├── B/                      # Command Line Assignment
├── C/                      # JSON Assignment
├── D/                      # GUI Assignment
├── E/                      # TCP Assignment
├── Fish/                   # Fish Project Directory
│   ├── Admin/              # Source code for the manager and referee classes
│   ├── Common/             # Source code for the game state
│   ├── Other/              # Unit testing directory
│   ├── Planning/           # All planning memos, and self evaluations
│   ├── Player/             # Source code for the AI player
│   ├── Remote/             # Source code for the adapters and proxies needed for remote play
│   └── README.md           # README for Fish Project, details methods, classes, etc
├── Other/                  # Contains JSON parsing code used for integration testing
└── README.md               # This README file
```
