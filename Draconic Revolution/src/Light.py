import pygame as pg


class Light:
	def __init__(self, level, size=64):
		self.size = size
		self.image = pg.Surface((size,size))
		self.image.fill((0,0,0), special_flags=pg.BLEND_ADD)

		if(level == -1):
			level = 0
			
		self.image.set_alpha(level)