# Light Protocol

All events assume `NOTE_ON` as an input. Nothing occurs, when `NOTE_OFF` is received.

| MIDI Channel | MIDI Note | Light Event | Argument (MIDI Event) | Comment |
|:---|:---|:---|:---|:---|
|1|`0`|BLACKOUT|`duration: 0v=30ms 100+v=10_000ms`|All bulbs shut down|
|any|`12`|GO|`duration: 0v=30ms 100+v=10_000ms`|Bulbs within given group receive preset command|
|any|`13`|BRIGHTNESS|`brightness: 0v=0 100+v=100`|Set brightness to bulbs within given that group on the next `GO`|
|any|`14`|WHITE|`temperature: 0v=2700K 127v=5500K`|Set bulbs to white mode and preset temperature on the next `GO`|
|any|`15`|RED|`red: 0v=0 127v=127`|Set bulbs to RGB mode and register this portion of red color on the next `GO`|
|any|`16`|GREEN|`red: 0v=0 127v=127`|Set bulbs to RGB mode and register this portion of green color on the next `GO`|
|any|`17`|BLUE|`red: 0v=0 127v=127`|Set bulbs to RGB mode and register this portion of blue color on the next `GO`|
