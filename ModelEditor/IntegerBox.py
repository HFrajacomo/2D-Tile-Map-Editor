import pygame as pg

from Bevel import Bevel

class IntegerBox:
	num = 0
	bev = None
	font = None
	size = 0
	pos = None

	def __init__(self, size, pos, color):
		self.bev = Bevel(size*2, size, color, pos)
		self.size = size
		self.font = pg.font.SysFont("arial.ttf", 40)
		self.pos = pos


	def change_value(self, screen, val):
		if(self.num + val >= 255):
			self.num = 255
		elif(self.num + val <= 0):
			self.num = 0
		else:
			self.num += val

		self.bev.fill()
		self.bev.surf.blit(self.font.render(str(self.num), False, (255,255,255)), (self.size/10, self.size/10))
		self.bev.draw(screen)
		pg.display.update(pg.Rect((self.pos), (self.size*2,self.size)))

	def reset(self, screen):
		self.num = 0

		self.bev.fill()
		self.bev.surf.blit(self.font.render(str(self.num), False, (255,255,255)), (self.size/10, self.size/10))
		self.bev.draw(screen)
		pg.display.update(pg.Rect((self.pos), (self.size*2,self.size)))

	def get_value(self):
		return self.num

def tupsum(tx, ty):
	return (tx[0]+ty[0], tx[1]+ty[1])