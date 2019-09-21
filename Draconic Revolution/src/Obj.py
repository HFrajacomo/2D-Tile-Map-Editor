import pygame as pg


class Obj:

	def __init__(self, id, size=32, scaling=2):
		self.size = size
		self.image = pg.image.load(get_obj_index(id))
		self.get_frame_zero()
		if(scaling != 1):
			self.scale(scaling)

	def scale(self, x):
		self.image = pg.transform.scale(self.image, (self.size*x, self.size*x))

	def get_frame_zero(self):
		if(self.image.get_size()[0]>32):
			self.image = self.image.subsurface(pg.Rect((0,0), (32,32)))

class AnimatedObj:
	def __init__(self, id, frame, size=32, scaling=2):
		self.id = id
		self.size = size
		self.image = None
		self.scale(scaling, frame)

	def scale(self, x, frame):
		if(x != 1):
			self.image = pg.transform.scale(pg.image.load(get_obj_index(self.id)).subsurface(pg.Rect((frame*self.size, 0), (self.size,self.size))), (self.size*x,self.size*x))
		else:
			self.image = pg.image.load(get_obj_index(self.id)).subsurface(pg.Rect((frame*self.size, 0), (self.size,self.size)))



def get_obj_index(id):
	if(id <= 0):
		return "src\\Objects\\none.png"

	ref = open("src\\Objects\\Obj_ref", "r")
	data = ref.read()
	return "src\\Objects\\" + data.split("\n")[id] + ".png"
