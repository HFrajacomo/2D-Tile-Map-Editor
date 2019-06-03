import pygame as pg

from Bevel import Bevel

class CoordBox:
	coord = None
	bev = None
	font = None
	size = 0
	pos = None

	def __init__(self, size, pos, color):
		self.bev = Bevel(size*4, size, color, pos)
		self.size = size
		self.font = pg.font.SysFont("arial.ttf", 40)
		self.pos = pos

	def change_value(self, screen, pos, TiledMap):
		self.coord = [pos[0], pos[1]]

		self.bev.draw(screen)
		screen.blit(self.font.render(str(self.coord), False, (0,0,0)), (self.pos[0]+2, self.pos[1]+2))
		pg.display.update(pg.Rect((self.pos), (self.size*4,self.size)))
