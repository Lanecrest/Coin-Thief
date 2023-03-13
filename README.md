# Coin-Thief

Coin Thief is a Python game that uses only default modules but relies on Windows. The object is to move around a procedurally generated playing area to collect coins and increase your score while avoiding the enemy.

About
===
This is my first attempt making a game in Python. It is inspired 
by a very basic game I made on my TI-83+ using TI-BASIC back in
2001. It is the realized version of a project started long ago!

The design goal is to keep the game on the more basic side by 
only using default modules and only using the command line to 
display. It will only run on Windows however, due to some of the 
default modules being used.

Screenshots
===
![Alt text](/screenshots/v1_41_title.png?raw=true "Title Screen")
![Alt text](/screenshots/v1_41_settings.png?raw=true "Settings Screen")
![Alt text](/screenshots/v1_41_gameplay.png?raw=true "Gameplay")

High Score File
===
The game should create the high score file if it doesn't exist 
or gets deleted. If it gets corrupted, the structure should 
look like this, between the dashes. Changing the 0s to any
other number will make the game think that is your high score.

-----
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

-----

Credits
===
Programmed by Lanecrest Tech
