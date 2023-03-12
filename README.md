# Coin-Thief
Python console game

Coin Thief v1.41

CHANGELOG:
===
1.41
==
-Added more sound effects

1.4
==
-Changed scoring slightly for regular modes
-Added Endless Mode

1.3
==
-Updated spawning logic to (hopefully) prevent softlocks
-Allow settings to be changed between games

1.2
==
-Updated High Score file system
-Updated level display code (no longer flashes)

1.1
==
-Added Sound

1.0
==
-Initial Release

ABOUT:
===
This is my first attempt making a game in Python. It is inspired 
by a very basic game I made on my TI-83+ using TI-BASIC back in
2001. It is the realized version of a project started long ago :)

The design goal is to keep the game on the more basic side by 
only using default modules and only using the command line to 
display. It will only run on Windows however due to some of the 
default modules being used.

HIGH SCORE FILE:
===
The game should create the high score file if it doesn't exist 
or gets deleted. If it gets corrupted, the structure should 
look like this, between the dashes. Changing the 0s to any
other number will make the game think that is your high score.

[Score]

easy_small = 0

easy_medium = 0

easy_hard = 0

normal_small = 0

normal_medium = 0

normal_large = 0

hard_small = 0

hard_medium = 0

hard_large = 0

endless_endless = 0


CREDITS:
===
©2023 Lanecrest Tech
As this is a Python script you are free to view the source, 
modify, and redistribute as you see fit. I just ask that if
you had any fun, you give me some props :)
