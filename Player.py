import pygame
from Pong_Constants import blue

class Player(object):
	""" The paddle for the Pong game

	Attributes:
		attributes : holds the current players size, width, speed, color, and controls
						for easy access mapping to them via __setitem__ and __getitem__
		PLAYER_SIZE : (width, height) tuple, default size of player
		SPEED : An integer default speed of the player
		CONTROLS : A dictionary for the default controls of the player
		PLAYER_1, PLAYER_2 : enum for the other player
	"""
	PLAYER_SIZE = width, height = 20,130
	SPEED = 5
	CONTROLS = {'down':pygame.K_DOWN, 'up':pygame.K_UP}
	PLAYER_1 = 0
	PLAYER_2 = 1

	def __init__(self, name, parent, playerNumber,**kwargs):
		self.attributes = {
			'color': blue,
			'size' : self.PLAYER_SIZE,
			'speed' : self.SPEED,
			'width' : self.width,
			'height' : self.height,
			'controls': self.CONTROLS
		}

		self.set_attributes(kwargs)
		self.parent = parent
		self.name = name
		self.playerNumber = playerNumber
		self.points = 0
		
		self.__paddle_init()

	def __setitem__(self, key, value):
		self.attributes[key] = value
	
	def __getitem__(self, key):
		if key in self.attributes.keys():
			return self.attributes[key]
		else:
			return None
	def __str__(self):
		if(self.playerNumber == Player.PLAYER_1):
			return "Player 1"
		return "Player 2"

	def __paddle_init(self):
		"Sets position of the player according to the playerNumber"
		self.rect = pygame.Rect(0,0,0,0)
		self.update()
		self.rect.width, self.rect.height = self.PLAYER_SIZE

	def draw(self):
		"Draws player"
		self.__control_handler()
		pygame.draw.rect(self.parent.screen, self['color'], self.rect)

	def add_point(self):
		"add one point to player"
		self._points += 1

	def __move_up(self):
		"moves player up"
		if(10 < self.rect.y):
			self.rect.move_ip(0, -self['speed'])
	def __move_down(self):
		"moves player down"
		if(self.parent.screen.get_height() - self.height - 10 > self.rect.y):
			self.rect.move_ip(0, self['speed'])

	def __control_handler(self):
		"Checks if buttons for player are being pressed"
		keyDown = pygame.key.get_pressed()
		controls = {self['controls']['down']:self.__move_down, 
					self['controls']['up']:self.__move_up}
		for key, func in controls.items():
			if(keyDown[key]):
				func()
	def get_points(self):
		"Returns a string representation of the players points"
		return self._points

	def set_points(self, val):
		"Sets the points value"
		if(val >= 0):
			self._points = val
		else:
			raise ValueError("Points value can't be negative.")


	def update(self):
		"updates players on resize of screen"
		if (self.playerNumber == Player.PLAYER_1):
			position = (10, self.parent.get_screen_center(Y=True)) 
		else: 
			position = (self.parent.screen.get_width() - self.width - 10, self.parent.get_screen_center(Y=True))
		self.rect.center = position;


	def set_attributes(self, kwargs):
		"Sets the attributes of Player from kwargs item"
		for attr in ['color', 'position', 'width', 'height', 'controls']:
			if( attr in kwargs.keys()):
				self[attr] = kwargs[attr]
	def reset(self):
		"Resets players point and position"
		self.points = 0
		self.update()

	points = property(get_points, set_points)



