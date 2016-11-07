import pygame
import sys
from Ball import Ball
from Menu import Menu
from Menu import MenuOption
from Player import Player
from Pong_Constants import *
from SoundManager import SoundManager
from TextHandler import TextHandler


class Pong:
	"""
	Handles drawing of all components. 
	players -> Players[] list of players
	ball -> Ball ball to be bouncing in Pong
	scoreboard -> TextHandler scoreboard displayed on screen
	state -> boolean[] a list of booleans representing each state of the game
	MAX_POINTS -> the max points by default 
	"""
	SETTINGS = {
		"MAX_POINTS" : 8,
		"players" : [
			{
				"name":"Player 1",
				"color": (255,9,9)
			},
			{
				"name":"Player 2",
				"color": (40,40,255)	
			}
		]
	}
	DEFAULT_SIZE = width, height = 600,600
	FONT_SIZE = 52
	MAX_POINTS = 2
	soundFiles = ["paddle.wav", "point.wav", "winning_song.wav"]
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Pong: Leon")

		self.screen = pygame.display.set_mode(self.DEFAULT_SIZE, pygame.RESIZABLE)
		self.__init_players()
		self.__init_sound()
		self.__init_menus()
		
		self.ball = Ball(self, self.players, speed=9)
		self.scoreboard = TextHandler(self, self.players)
		self.state = [False for state in GameState.states.keys()]
		self.set_game_state_to(GameState.states["START"])
		
		#menus

	def __init_menus(self):
		"Setups menus"
		startMenu = Menu(self, "Start Menu")
		startOption = MenuOption(self, "Start", self.start_game)
		exitOption = MenuOption(self, "Exit", quit)
		startMenu.addOption(startOption)
		startMenu.addOption(exitOption)

		self.set_current_menu(startMenu)

	def __init_players(self):
		"Initializes players"
		self.players = [Player("Player 1", self, Player.PLAYER_1, color=(255,9,9), controls={'up':pygame.K_w, 'down':pygame.K_s}), 
						Player("Player 2", self, Player.PLAYER_2)]
		self.currentWinner = None
	
	def __init_sound(self):
		"Initialize SoundManager"
		self.sound = SoundManager(self.soundFiles)

	def draw(self):
		"""
			Draws all components of the game.	
		"""
		self.screen.fill(black)
		
		if(self.state[GameState.states["PLAY"]]):
			self.__draw_players()
			self.__draw_middle_lines()
			self.scoreboard.draw()
			self.ball.draw()
			#middle line
		elif(self.state[GameState.states["PAUSE"]]):
			self.scoreboard.draw_pause()
		elif(self.state[GameState.states["START"]]):
			self.draw_current_menu()
		elif(self.state[GameState.states["WINNER"]]):
			self.scoreboard.draw_winner(self.currentWinner)
			
		
		self.event_check()
		self.check_option_hover()
		pygame.display.flip()
		self.__control_handler()

	def __draw_players(self):
		"draws players in game"
		for player in self.players:
				player.draw()

	def __draw_middle_lines(self):
		"""Draws middle white lines and colored player lines
		Colored player lines represent how far the player is from winning.
		"""
		screenHeight = self.screen.get_height()
		screenWidth = self.screen.get_width()
		screenCenterX = self.get_screen_center(X=True);
		
		#player1 progress
		player1 = self.players[Player.PLAYER_1]
		percentageToMaxPoints = float(Pong.MAX_POINTS - player1.points)/Pong.MAX_POINTS;
		pygame.draw.line(self.screen, 
						player1["color"], 
						(screenCenterX - 3, screenHeight * percentageToMaxPoints), 
						(screenCenterX - 3, 
						self.screen.get_height()), 
						3)
		#middleline
		pygame.draw.line(self.screen, white, (self.get_screen_center(X=True), 0), (self.get_screen_center(X=True), self.screen.get_height()))
		
		#player2 progress
		player2 = self.players[Player.PLAYER_2]
		percentageToMaxPoints = float(Pong.MAX_POINTS - player2.points)/Pong.MAX_POINTS;
		pygame.draw.line(self.screen, 
						player2["color"], 
						(screenCenterX + 3, screenHeight * percentageToMaxPoints), 
						(screenCenterX + 3, 
							screenHeight), 
						3)

	def set_game_state_to(self, gameState):
		"Sets the game state"
		#set all to false
		for i, state in enumerate(self.state):
			self.state[i] = False

		self.state[gameState] = True

	def __control_handler(self):
		keyDown = pygame.key.get_pressed()
		if(keyDown[pygame.K_p]):
			self.pause()
		elif(keyDown[pygame.K_RETURN]):
			if (self.state[GameState.states["START"]]): 
				self.ball.start_count_down()
				self.play()
			if (self.state[GameState.states["WINNER"]]):
				self.restart()
		elif(keyDown[pygame.K_ESCAPE] and not self.state[GameState.states["PLAY"]]):
			quit()

	def pause(self):
		"Pauses the game"
		self.set_game_state_to(GameState.states["PAUSE"])

	def play(self):
		"Continues the game"
		self.set_game_state_to(GameState.states["PLAY"])

	def start_game(self):
		"Starts game from beginning"
		self.set_game_state_to(GameState.states["PLAY"])
		self.ball.start_count_down()

	def get_screen_center(self, **kwargs):
		"""
		Returns a tuple of the screen center by default
		if X is set it returns just the widths middle
		if Y is set it returns just the widths middle
		if X and Y are set to True it returns the default tuple
		"""
		widthCenter = self.screen.get_width()/2
		heightCenter = self.screen.get_height()/2
		if("X" in kwargs and "Y" in kwargs):
			return (widthCenter, heightCenter)
		if("X" in kwargs):
			return widthCenter
		if("Y" in kwargs):
			return heightCenter
			
		return (widthCenter, heightCenter)


	def set_current_menu(self, menu):
		"Sets the current menu to be drawn"
		self.currentMenu = menu

	def draw_current_menu(self):
		"Draws the current menu"
		title = self.currentMenu.title
		options = self.currentMenu.options

		#draw menu title
		if(pygame.font):
			font = pygame.font.Font(None, self.FONT_SIZE)
	        text = font.render(title, 1, (255, 255, 255))
	        textpos = text.get_rect(centerx=self.get_screen_center(X=True), centery=self.get_screen_center(Y=True)/4)
	        self.screen.blit(text, textpos)
	    #draw menu options
		for i, option in enumerate(options):
			if(pygame.font):
				font = pygame.font.Font(None, self.FONT_SIZE)
		        text = font.render(option.text, 1, option.color, option.background)
		        xPosition = self.get_screen_center(X=True)
		        yPosition = (self.get_screen_center(Y=True)/2) + (self.FONT_SIZE + 10)*i
		        option.set_rect(text.get_rect(centerx=xPosition, centery=yPosition))
		        self.screen.blit(text, option.get_rect())

	def event_check(self):
		for e in pygame.event.get():
			if(e.type == pygame.QUIT) : self.close()

			if (e.type == pygame.MOUSEBUTTONUP):
				self.check_option_clicked()
			if (e.type == pygame.VIDEORESIZE):
				self.screen = pygame.display.set_mode(e.size, pygame.RESIZABLE)
				self.update()

	def check_option_hover(self):
		"Checks if a menu option is hovered and does a hover effect if true"
		mousePos = pygame.mouse.get_pos()
		for option in self.currentMenu.options:
			if(option.get_rect().collidepoint(mousePos)):
				option.hover(True)
			else: 
				option.hover(False)

	def check_option_clicked(self):
		"Checks if a menu option in the currentMenu is clicked and performs action if so"
		mousePos = pygame.mouse.get_pos()
		for option in self.currentMenu.options:
			if(option.get_rect().collidepoint(mousePos)):
				option.action()

	def check_for_winner(self):
		"Checks if there is a winner and sets game state to winner is so"
		for player in self.players:
			if(player.points == Pong.MAX_POINTS):
				self.currentWinner = player
				self.play_sound(Sounds.WIN)
				self.set_game_state_to(GameState.states["WINNER"])

	def update(self):
		"Calls update methods for when window resizes"
		for player in self.players:
			player.update()
		self.ball.update()

	def play_sound(self, sound):
		self.sound.play(self.soundFiles[sound])


	def restart(self):
		"Reset the game points and players"
		for player in self.players:
			player.reset()
		self.ball.reset()
		self.currentWinner = None
		self.set_game_state_to(GameState.states["START"])

	def close(self):
		"Closes application and does cleanup if needed"
		quit()