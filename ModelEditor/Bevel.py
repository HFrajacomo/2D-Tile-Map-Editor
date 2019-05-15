import pygame as pg

class Bevel:
	surf = ""
	bg_color = ""
	pos = ()

	def __init__(self, width, height, rgb, pos):
		self.surf = pg.Surface((width, height))
		self.bg_color = rgb
		self.surf.fill(rgb)
		self.pos = pos

	def draw(self, screen):
		screen.blit(self.surf, self.pos)

	def fill(self):
		self.surf.fill(self.bg_color)

	def get_size(self):
		return self.surf.get_size()
