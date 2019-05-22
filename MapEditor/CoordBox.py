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
		self.font = pg.font.SysFont("arial.ttf", 24)
		self.pos = pos

	def change_value(self, screen, pos, TiledMap):
		self.coord = tuple([pos[1] + TiledMap.win_cord[0], pos[0] + TiledMap.win_cord[1]])

		self.bev.draw(screen)
		screen.blit(self.font.render(str(self.coord), False, (255,255,255)), (self.pos[0]+2, self.pos[1]+2))
		pg.display.update(pg.Rect((self.pos), (self.size*4,self.size)))
