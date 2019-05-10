import pygame as pg

class Bevel:
	surf = ""
	bg_color = ""

	def __init__(self, width, height, rgb):
		self.surf = pg.Surface((width, height))
		self.bg_color = rgb
		self.surf.fill(rgb)

	def draw(self, screen, pos):
		screen.blit(self.surf, (pos[0], pos[1]))
