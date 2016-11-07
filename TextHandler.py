import pygame
from Player import Player

class TextHandler(object):
	"""
	Draws the various text on the screen for Pong game.
	players -> Players[] list of players
	screen -> pygame.Surface screen to draw Score Board on

	"""
	DEFAULT_SIZE = 36
	SCORE_SIZE = 600
	WINNER_SIZE = 80
	def __init__(self, parent, players):
		self.parent = parent
		self.players = players
	def draw(self):
		"""
		Draws components for scoreboard
		"""
		self.draw_score()
			
	def draw_score(self):
		#player1 score
		if(pygame.font):
			player = self.players[Player.PLAYER_1]
			font = pygame.font.Font(None, self.SCORE_SIZE)
	        text = font.render(str(player.get_points()), 1, player["color"])
	        textpos = text.get_rect(centerx=self.parent.screen.get_width()/4)
	        self.parent.screen.blit(text, textpos)
	    #player2 score
		if(pygame.font):
			player = self.players[Player.PLAYER_2]
			font = pygame.font.Font(None, self.SCORE_SIZE)
	        text = font.render(str(player.get_points()), 1, player["color"])
	        textpos = text.get_rect(centerx=self.parent.screen.get_width()*3/4)
	        self.parent.screen.blit(text, textpos)
	    #time
		if(pygame.font):
			font = pygame.font.Font(None, self.DEFAULT_SIZE)
	        text = font.render(str(pygame.time.get_ticks()/1000.00), 1, (255, 255, 255))
	        textpos = text.get_rect(centerx=self.parent.screen.get_width()*3/4, centery=self.parent.screen.get_height() - self.DEFAULT_SIZE)
	        self.parent.screen.blit(text, textpos)

	def draw_pause(self):
		"Draws pause menu"
		if(pygame.font):
			font = pygame.font.Font(None, self.DEFAULT_SIZE)
	        text = font.render(str(self.players[0].get_points()) + " Score " + self.players[1].get_points(), 1, (255, 255, 0))
	        pauseText = font.render("Paused", 1, (200, 255, 200))
	        textpos = text.get_rect(center=(self.parent.screen.get_width()/2, (self.parent.screen.get_height()/2)))
	        textpause = text.get_rect(centerx=(self.parent.screen.get_width()/2))
	        self.parent.screen.blit(text, textpos)
	        self.parent.screen.blit(pauseText, textpause)
	        
	def draw_winner(self, player):
		"Draws the tex for the winning player"
		#check if player won
		if(player == None):
			self.parent.set_game_state_to(GameState.states["START"])

		elif(pygame.font):
			font = pygame.font.Font(None, self.WINNER_SIZE)
			text = font.render(str(player) + " WON!", 1, player["color"])
			textpos = text.get_rect(center=(self.parent.screen.get_height()/2, self.parent.screen.get_height()/2))

			self.parent.screen.blit(text, textpos)
