import pygame as py
import time
from Declaration import *

class SoundHandler():

	def __init__(self):
		py.mixer.init()
		py.time.delay(1000)
		py.mixer.music.set_volume(8)
		self.name = None

	def loadMUSIC(self, name):
		py.mixer.music.load(const.PATH+const.MUSICFILE+name+".mp3")
		self.name = name
		self.set_volume(0.5)

	def play(self):
		print('play')
		py.mixer.music.play()

	def stop(self):
		py.mixer.music.stop()

	def rewind(self):
		py.mixer.music.rewind()

	def pause(self):
		py.mixer.music.pause()

	def unpause(self):
		py.mixer.music.unpause()

	def set_volume(self, volume):
		py.mixer.music.set_volume(volume)

	def set_pos(self):
		py.mixer.music.set_pos()

	def get_volume(self):
		return py.mixer.music.get_volume()

	def isPlaying(self):
		return py.mixer.music.get_busy()
	def get_volume():
		return py.mixer.music.get_volume()

	def getName(self):
		return self.name
