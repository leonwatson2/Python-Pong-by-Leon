import pygame
import math
import random
import os.path
from Player import Player
from Pong_Constants import Direction, white, Sounds

class Ball(Player):
	""" The ball for the Pong game

	Attributes:
		attributes : holds the current players size, width, speed, color, and controls
						for easy access mapping to them via __setitem__ and __getitem__
		BALL_SIZE : (width, height) tuple, default size of player
		SPEED : An integer default speed of the player
		MAX_ANGLE : integer in degrees, The max angle the ball can bounce off paddle
		COUNT_DOWN_TIME : integer in seconds, the amount of time the ball pauses before starting a point
	"""
	RADIUS = 10
	SPEED = 6
	BALL_SIZE = 15, 15
	MAX_ANGLE = 66 #degrees
	COUNT_DOWN_TIME = .75 #seconds
	def __init__(self, parent, players, **kwargs):
		self.parent = parent
		self.players = players
		self.direction = {'Vertical':Direction.UP,'Horizontal':Direction.LEFT}
		self.attributes = {
			'color': white,
			'position': (self.parent.screen.get_width()//2, self.parent.screen.get_height()//2),
			'size' : self.RADIUS,
			'speed' : self.SPEED,
			'width' : self.width,
			'height' : self.height,
		}
		self.velocity = [self.SPEED, 0]
		Player.set_attributes(self, kwargs)
		self.rect = pygame.Rect(0,0,0,0)
		self.rect.center = self['position']
		self.rect.width, self.rect.height = self.BALL_SIZE
		self.lastChangeInDirection = 0
		self.paddleCollisions = 0
		
	def draw(self):
		"draws ball, checks collsions, checks if ball countdown was reset"
		if not self.is_counting_down(): self.move()
		self.check_collisions()
		pygame.draw.rect(self.parent.screen, self['color'], self.rect)

	def move(self):
		"Moves ball"
		self.rect.move_ip(self.velocity)

	def check_collisions(self):
		"Checks ball collisions of walls and players"
		#top and bottom wall collisions
		hitTopWall = self.rect.y < 0 and self.going(Direction.UP)
		hitBottomWall = self.rect.y + self.rect.width > self.parent.screen.get_height() and self.going(Direction.DOWN)
		if(hitTopWall or hitBottomWall): 
			self.toggle_direction()
		
		#side wall collision	
		hitLeftWall = self.rect.x < 0 and self.going(Direction.LEFT)
		hitRightWall = self.rect.x + self.rect.width > self.parent.screen.get_width() and self.going(Direction.RIGHT)
		if(hitLeftWall or hitRightWall):
			self.reset()

			if(hitLeftWall):
				self.players[1].add_point()
			else:
				self.players[0].add_point()
			self.parent.check_for_winner()
			self.play_sound(Sounds.POINT)

		#player collisions
		for player in self.players:
			if(self.rect.colliderect(player.rect)):
				self.get_new_velocity(player)
				self.play_sound(Sounds.PADDLE)

	def toggle_direction(self):
		"Toggle the up/down direction of the ball"
		self.velocity[1] = -self.velocity[1]

	def get_new_velocity(self, player):
		"Changes velocity of ball according to where it hit the player's paddle"
		if(not self.has_collided()):
			paddle = player.rect
			ball = self.rect
			offsetFromMiddle = (paddle.y+paddle.height/2) - ball.y
			normalizedIntersection = offsetFromMiddle/float(paddle.height/2) 
			bounceangle = normalizedIntersection * (self.MAX_ANGLE/15)*math.pi/12
			if(self.going(Direction.LEFT)):
				velocityx = self.SPEED * math.cos(bounceangle)
			else:
				velocityx = -self.SPEED * math.cos(bounceangle)
			
			self.velocity = [velocityx, self.SPEED * -math.sin(bounceangle)]
			self.lastChangeInDirection = pygame.time.get_ticks()

	def has_collided(self):
		"Test if the ball has collided in the last 100ms"
		return pygame.time.get_ticks() - (self.lastChangeInDirection + 200) < 0 

	def going(self, direction):
		"""
		Test if ball is going in a certain direction.
		direction -> Direction is the direction to check. 
		"""
		if(direction == Direction.LEFT):
			return self.velocity[0] < 0
		elif(direction == Direction.RIGHT):
			return self.velocity[0] > 0
		if(direction == Direction.UP):
			return self.velocity[1] < 0
		if(direction == Direction.DOWN):
			return self.velocity[1] > 0

	def play_sound(self, sound):
		"Plays sound specified"
		self.parent.sound.play(self.parent.soundFiles[sound])

	def is_counting_down(self):
		"Test if the ball count down is done"
		return self.endTime > pygame.time.get_ticks()

	def start_count_down(self):
		"Sets the count down attribute and endTime"
		self.endTime = pygame.time.get_ticks() + self.COUNT_DOWN_TIME * 1000

	def update(self):
		"Updates the reset position of ball"
		self['position'] = self.parent.get_screen_center()
		self.SPEED = self.parent.screen.get_width() * self.SPEED/self.parent.width

	def reset(self):
		"Resets the position of ball, sets to a psuedo random direction, starts countdown"
		self.rect.center = self['position']
		self.velocity = [random.randrange(-1,1,2)*self.SPEED, 0]
		self.start_count_down()

		#TODO winning screen and sound
