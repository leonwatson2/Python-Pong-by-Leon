import pygame

"""
This module contains classes used in Leon Pong.

"""

class Menu(object):
	"""
	Generic class for menus in game that holds menuoptions
	game -> Pong game this menu belongs to
	title -> String title of menu
	options -> MenuOptions[] a list of menu options for this menu
	"""
	def __init__(self, game, title):
		self.game = game
		self.title = title
		self.options = []

	def addOption(self, menuOption):
		"Add menu options to menu"
		self.options.append(menuOption)



	 
class MenuOption(object):
	"""
	An Options for a menu
	game -> Pong game that the menu belongs 
	text -> String text for the option
	action -> function thing to do if option is clicked
	rect -> pygame.Rect for reference
	link -> {previous:MenuOption, next:MenuOption} an optional next menu and previous link
	""" 
	def __init__(self, game, text, action, **kwargs):
		self.game = game
		self.text = text
		self.action = action
		if("link" in kwargs):
			self.link = link
		self.hover(False)
	
	def set_rect(self, rect):
		"Sets Rect object of menu option"
		if(isinstance(rect, pygame.Rect)):
			self.rect = rect
		else: 
			raise Exception("Rectangle was not passed to set_rect() in MenuOption class.")

	def get_rect(self):
		"Returns Rect object of menu option"
		return self.rect
	
	def hover(self, isHovering):
		if(isHovering):
			self.color = (0,0,0)
			self.background = (255,255,255)
		else:	
			self.color = (255,255,255)
			self.background = (0,0,0)

