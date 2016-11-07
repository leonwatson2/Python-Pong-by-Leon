import pygame
import os

class SoundManager(object):
	""" 
	Manages sounds to be played
	Attributes:
		soundFiles: a dictionary of pygame.mixer.Sound of the sounds 
		_curentSong : returns the tuple (name, Sound) currently playing
	"""
	SOUND_DIR = "data"
	def __init__(self, soundFiles):
		
		pygame.mixer.init(22050)
		pygame.mixer.set_num_channels(6)
		self._currentSong = None
		self.soundFiles = dict([self.get_sound_tuple(soundFile) for soundFile in soundFiles])
		print(self.soundFiles)

	def play(self, fileName):
		"Plays sound with the fileName"
		print("get_busy" + str(pygame.mixer.get_busy()))
		print("get_num_channels" + str(pygame.mixer.get_num_channels()))
		if(self._currentSong): self.currentSong[1].stop()
		for name,sound in self.soundFiles.items():
			if(name == fileName):
				sound.play()
				self.currentSong = (name,sound)				
				return sound


	def get_sound_tuple(self, fileName):
		"create a tuple with file name and Sound object"
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		filepath = os.path.join(main_dir, self.SOUND_DIR, fileName)
		return (fileName, pygame.mixer.Sound(filepath))

	@property
	def currentSong(self):
		return self._currentSong

	@currentSong.setter
	def currentSong(self, value):
		self._currentSong = value
