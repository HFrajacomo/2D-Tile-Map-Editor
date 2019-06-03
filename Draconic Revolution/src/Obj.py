import pygame as pg


class Obj:
	image = []
	size = 32

	def __init__(self, id, size=32, scaling=2):
		self.size = size
		self.image = pg.image.load(get_tile_index(id))
		if(scaling != 1):
			self.scale(scaling)

	def scale(self, x):
		self.image = pg.transform.scale(self.image, (self.size*x, self.size*x))

def get_tile_index(id):
	if(id <= 0):
		return "src\\Objects\\none.png"

	ref = open("src\\Objects\\Obj_ref", "r")
	data = ref.read()
	return "src\\Objects\\" + data.split("\n")[id] + ".png"
