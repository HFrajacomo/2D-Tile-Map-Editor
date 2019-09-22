import pyglet as pg
from pyglet.gl import *

class Obj:

	def __init__(self, id, frame, size=32, scaling=2):
		self.size = size
		self.image = pg.image.load(get_obj_index(id)).get_texture()
		if(scaling != 1):
			self.scale(scaling)

	def scale(self, x):
		glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)  
		self.image.width = self.size*x
		self.image.height = self.size*x
 
class AnimatedObj:
	def __init__(self, id, frame, size=32, scaling=2):
		self.id = id
		self.size = size
		self.image = None
		self.image = pg.image.load(get_obj_index(id)).get_texture()
		self.scale(scaling, frame)

	def scale(self, x, frame):
		self.image = self.image.get_region(frame*self.size,frame*self.size, self.size, self.size)
		glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)  
		self.image.width = self.image.width*x
		self.image.height = self.image.height*x


def get_obj_index(id):
	if(id <= 0):
		return "src\\Objects\\none.png"

	ref = open("src\\Objects\\Obj_ref", "r")
	data = ref.read()
	return "src\\Objects\\" + data.split("\n")[id] + ".png"


# Animated Objects

'''

UPDATE THIS CODELIST EVERYTIME YOU ADD A NEW ANIMATED OBJECT

'''
animated_obj_codelist = [600,601,602]

# Generates Dictionary
animated_obj_dictionary = [{},{}]

for element in animated_obj_codelist:
	animated_obj_dictionary[0][element] = AnimatedObj(element,0).image
	animated_obj_dictionary[1][element] = AnimatedObj(element,1).image

### All Objects

all_obj_img = {}

for i in range(0,9999):
	try:
		if(i not in animated_obj_dictionary[0].keys()):
			all_obj_img[i] = Obj(i,0).image
	except IndexError:
		break

