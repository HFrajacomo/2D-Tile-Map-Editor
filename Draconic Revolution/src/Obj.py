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

class GeneralObj:
	id = None
	def __init__(self, id):
		self.hp = None
		self.solid = None
		self.transparency = None

	# Overload function
	# Code to be run when player interacts with block
	def action(self, entity):
		pass

	# Overload function
	# Code to be run when entity walks onto block
	def step_on(self, entity):
		pass

	# Overload function
	# Code to be run when examined block (may add general and specialist's examiniation)
	def examine(self, entity):
		pass

	# Overload function
	# Code to be run when block is attacked (works with solid only)
	def attacked(self, entity):
		pass

	# Overload function
	# Shows crafting recipe for block
	def recipe(self, entity):
		pass

	# Returns the image of tile to be blitted
	# IMPLEMENT RESIZING ABILITY
	def surface(self):
		return pg.image.load(get_tile_index(self.id))

class NoneObj(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 1
		self.solid = False
		self.transparency = True

class VegetableStand(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 50
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "It contains lots of food"

class FoodBasket(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 50
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "It contains lots of food"

class Blackboard(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 120
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "Some chalk dust is on it's surface"

class ItemCrate(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 80
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "There are items inside"

class Crate(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 80
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "A solid wooden crate"

class EmptyCrate(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 50
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "There's only dust inside"

class Flower(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 15
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "A pretty nature's child"

class Logs(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 30
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "Some logs"

class Fountain(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 800
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "A beautiful fontain"

class Statue(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 500
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "I can recognize the image"

class GraveStone(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 300
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "It's old, you can barely read it"

class WoodenBarrel(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 100
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "I wonder what's inside..."

class Bucket(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 20
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "It's a bucket"

class Bush(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 100
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "Dense foliage"

class Chair(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 100
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "You can sit on it"

class Table(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 250
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "A plain table"

class Bed(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 400
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "Real comfy"

class Piles(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 500
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "There's a pile of stuff here"

class Hangings(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 50
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "Nice decoration"

class Altar(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 600
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "I can see candles and undecipherable symbols"

class Fence(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 50
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "Secure fence"

class Window(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 20
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "A glassy frame"

class Sign(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 50
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "There's something written on it"

class Pillar(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 800
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "Tough base"

class Stone(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 1000
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "A boulder"

class TallGrass(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 10
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "It has overgrown"

class Bookshelf(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 300
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "Books everywhere"

class SilverwoodTree(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 1500
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "A silvery tree with blue leaves"

class Stairs(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 2000
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "I wonder where it goes"

class LightPole(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 1000
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "Gives off light"

class Torch(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 10
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "Gives off light"

class Counter(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 200
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "A plain surface"

class Door(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 300
		self.solid = True
		self.transparency = False

	def examine(self, entity):
		return "You can open it"

class OpenDoor(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 300
		self.solid = False
		self.transparency = True

	def examine(self, entity):
		return "You can open it"

class Sack(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 10
		self.solid = True
		self.transparency = True

	def examine(self, entity):
		return "There's something inside"

class Anvil(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 5000
		self.solid = True
		self.transparency = True
		
	def examine(self, entity):
		return "A heavy iron anvil for blacksmithing"

class Forge(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 4000
		self.solid = True
		self.transparency = False
		
	def examine(self, entity):
		return "It's scorching hot"

class OakTree(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 2000
		self.solid = True
		self.transparency = False
		
	def examine(self, entity):
		return "A quiet calming Oak Tree"

class PineTree(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 2000
		self.solid = True
		self.transparency = False
		
	def examine(self, entity):
		return "A long Pine Tree"

class Cupboard(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 700
		self.solid = True
		self.transparency = False
		
	def examine(self, entity):
		return "There are stuffed with decoration"

class Bottle(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 5
		self.solid = False
		self.transparency = True
		
	def examine(self, entity):
		return "Some alcohol"

class Slider(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.hp = 1500
		self.solid = True
		self.transparency = True
		
	def examine(self, entity):
		return "Made for kids"

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
animated_obj_dictionary = [{},{},{}]

for element in animated_obj_codelist:
	animated_obj_dictionary[0][element] = AnimatedObj(element,0).image
	animated_obj_dictionary[1][element] = AnimatedObj(element,1).image
	animated_obj_dictionary[2][element] = AnimatedObj(element,2).image

### All Objects

all_obj_img = {}

for i in range(0,9999):
	try:
		if(i not in animated_obj_dictionary[0].keys()):
			all_obj_img[i] = Obj(i,0).image
	except IndexError:
		break

