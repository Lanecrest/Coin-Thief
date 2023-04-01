# Coin Thief

Coin Thief is a Python game that uses only default modules and runs entirely in the console. Due to several of the modules used, it will only run in Windows. The object is to move around a procedurally generated playing area to collect coins and increase your score while avoiding the enemy.

About
=
This is my first attempt making a game in Python. It is inspired 
by a very basic game I made on my TI-83+ using TI-BASIC back in
2001. It is the realized version of a project started long ago!

The design goal is to keep the game on the more basic side by 
only using default modules and only using the command line to 
display. It will only run on Windows however, due to some of the 
default modules being used.

[Screenshots](/screenshots)
=
![Alt text](/screenshots/v1_41_gameplay.png?raw=true "Gameplay")

[Change Log](CHANGELOG.md)
=

Requirements
=
There are no non-default modules used that don't come with a typical 
Python installation on Windows, which is one of the design goals. 
However, that means the game will only run correctly on Windows.

High Score File
=
The game will automatically create the [high_score.ini](high_score.ini) 
file in the same directory if it does not already exist so there should 
be no need to download/copy the file included in the repository. 
However, to demonstrate the file that is generated, I have included the 
default version. The values start at 0 and each setting is tracked 
separately. As you gain new high scores for each setting, the .ini 
will be updated. 

Road Map
=
This game was originally developed in January 2023 as a training 
exercise to develop Python programming skills. A major revision and 
refinement was initiated in April 2023 to be submitted for a Pygames 
contest. There are no plans to develop the game further past its 
submission for the Pygames.

Credits
=
Programmed by Lanecrest Tech
