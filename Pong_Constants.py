"""
This module provides constant and enums used in Leon Pong

"""

black = 0, 0, 0
blue = 40,40,255
white = 255,255,255
class Direction:
	"Enum for directions"
	UP = 1
	LEFT = 2
	RIGHT = 3
	DOWN = 4
class GameState:
	"Enum for states of game"
	states = {
	"PAUSE" : 0,
	"PLAY" : 1,
	"MENU" : 2,
	"START": 3,
	"WINNER": 4
	}
class Sounds:
	"Enum for sounds in game"
	PADDLE = 0
	POINT = 1
	WIN = 2