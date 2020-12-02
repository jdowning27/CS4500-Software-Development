# Remote

## Directory

```
.                                   # Remote directory
├── Adapters/                       # Holds adapter classes
│   ├── extended_referee.py         # Class extending the Referee class to add play_with(Colors[])
│   ├── course_to_legacy_player.py  # CoursePlayerInterface to PlayerInterface adapter class
│   └── legacy_to_course_player.py  # PlayerInterface to CoursePlayerInterface adapter class
├── Proxies/                        # Holds remote proxy classes
│   ├── remote_player_proxy.py      # RemotePlayerProxy class, handles TCP communication with remote players
│   └── server_proxy.py             # ServerProxy class, handles TCP communication with Fish.com servers
├── Other/                          # Holds the test classes for adapter and proxy classes
└── README.md                       # This README file
```

## TODO

* [X] update legacy PlayerInterface
* [X] extend referee to broadcast player colors
    * [X] test that play_with is called
    * [X] kick players that dont respond correctly
* [X] update manager to use generic referee
    * [X] test interface enforcement
* [X] Asyncio passed to referee and manager
    * [X] test timeouts
* [ ] create legacy -> course player adapter
    * [ ] test call translation
* [ ] create course -> legacy player adapter
    * [ ] test call translation
* [ ] create remote player proxy
    * [ ] test
* [ ] create server proxy
    * [ ] test
* [ ] create xclient that connects to server and creates server proxy / player
* [ ] create xserver that signs up players and makes the tournament using player proxies
* [ ] create integration tests
