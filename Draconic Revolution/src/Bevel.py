import pyglet as pg

class Bevel:
	def __init__(self, pos, filename):
		self.pos = pos
		self.image = pg.image.load(filename)

	def draw(self):
		sprite = pg.sprite.Sprite(self.image, x=self.pos[0], y=self.pos[1])
		sprite.draw()