from Tile import Tile
from Obj import Obj
import pygame as pg

class TileButton:
	hitbox = None
	tid = 0
	pos = []
	img = ""
	size = 0


	def __init__(self, pos, size, tile_id, mode, scaling=2):
		self.hitbox = pg.Rect(pos, (size,size))
		self.pos = pos
		self.tid = tile_id

		if(mode):
			self.img = Tile(tile_id).image
		else:
			self.img = Obj(tile_id).image

		self.size = size
		self.scale(scaling)

	def __str__(self):
		return str(self.tid)

	def __repr__(self):
		return str(self.tid)

	def __int__(self):
		return self.tid

	def click(self, pos):
		if(self.hitbox.collidepoint(pos[0], pos[1])):
			return self.tid
		else:
			return None

	def draw(self, screen):
		screen.blit(self.img, tuple(self.pos))
		pg.display.update(self.hitbox)

	def scale(self, x):
		self.img = pg.transform.scale(self.img, (self.size*x, self.size*x))
		self.hitbox = pg.Rect(tuple(self.pos), (self.size*x,self.size*x))