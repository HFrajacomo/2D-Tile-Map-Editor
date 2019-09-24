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
		self.id = id
		self.multiblock = False
		self.special_collision = False
		self.hp = None
		self.solid = None
		self.transparency = None

	# Overload function
	# Code to be run when player interacts with block
	def action(self, entity, pos, m, intermap):
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

	def __str__(self):
		return self.__class__.__name__ + ":" + str(self.id)

	def __repr__(self):
		return self.__class__.__name__ + ":" + str(self.id)

	# Easier to insert new special collision tiles with this
	def add_special_collision(self, list_of_ids):
		if(self.id in list_of_ids):
			self.solid = False
			self.special_collision = True
		else:
			self.solid = True

class NoneObj(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = None
		self.hp = 1
		self.solid = False
		self.transparency = True
		self.special_collision = False

class VegetableStand(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 50
		self.solid = True
		self.transparency = True
		self.special_collision = False		

	def examine(self, entity):
		return "It contains lots of food"

class FoodBasket(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 50
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "It contains lots of food"

class Blackboard(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 120
		self.solid = True
		self.transparency = False
		self.special_collision = False

	def examine(self, entity):
		return "Some chalk dust is on it's surface"

class ItemCrate(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 80
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "There are items inside"

class Crate(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 80
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "A solid wooden crate"

class EmptyCrate(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 50
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "There's only dust inside"

class Flower(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 15
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "A pretty nature's child"

class Logs(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 30
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "Some logs"

class Fountain(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 800
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "A beautiful fontain"

class Statue(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 500
		self.transparency = False
		self.solid = True
		self.special_collision = False

		# Special Collision
		self.add_special_collision([544])

	def examine(self, entity):
		return "I can recognize the image"

class GraveStone(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 300
		self.solid = True
		self.transparency = True
		self.special_collision = False

		self.add_special_collision([31,34])

	def examine(self, entity):
		return "It's old, you can barely read it"

class WoodenBarrel(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 100
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "I wonder what's inside..."

class Bucket(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 20
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "It's a bucket"

class Bush(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 100
		self.solid = True
		self.transparency = False
		self.special_collision = False

	def examine(self, entity):
		return "Dense foliage"

class Chair(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 100
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "You can sit on it"

class Table(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 250
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "A plain table"

class Bed(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 400
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "Real comfy"

class Piles(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 500
		self.solid = True
		self.transparency = False
		self.special_collision = False

	def examine(self, entity):
		return "There's a pile of stuff here"

class Hangings(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 50
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "Nice decoration"

class Altar(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 600
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "I can see candles and undecipherable symbols"

class Fence(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 50
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "Secure fence"

class Window(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 20
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "A glassy frame"

class Sign(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 50
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "There's something written on it"

class Pillar(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 800
		self.solid = True
		self.transparency = False
		self.special_collision = False

		self.add_special_collision([570])

	def examine(self, entity):
		return "Tough base"

class Stone(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 1000
		self.solid = True
		self.transparency = False
		self.special_collision = False

	def examine(self, entity):
		return "A boulder"

class TallGrass(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 10
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "It has overgrown"

class Bookshelf(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 300
		self.solid = True
		self.transparency = False
		self.special_collision = False

		self.add_special_collision([578,576,244,237,239,241])

	def examine(self, entity):
		return "Books everywhere"

class SilverwoodTree(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 1500
		self.solid = True
		self.transparency = False
		self.special_collision = False

		self.add_special_collision([595])

	def examine(self, entity):
		return "A silvery tree with blue leaves"

class Stairs(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 2000
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "I wonder where it goes"

class LightPole(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 1000
		self.solid = True
		self.transparency = True
		self.special_collision = False

		self.add_special_collision([598,599])

	def examine(self, entity):
		return "Gives off light"

class Torch(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 10
		self.solid = False
		self.transparency = True
		self.special_collision = True

	def examine(self, entity):
		return "Gives off light"

class Counter(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 200
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "A plain surface"

class Door(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 300
		self.solid = True
		self.transparency = False
		self.special_collision = False

	def examine(self, entity):
		return "You can open it"

	def action(self, entity, pos, m, intermap):
		if(self.id == 108): # Fancy door
			m.obj_grid[pos[1]][pos[0]] = 110
			intermap[pos[1]][pos[0]] = gen_obj(110)
		elif(self.id == 107): # Normal door
			m.obj_grid[pos[1]][pos[0]] = 603
			intermap[pos[1]][pos[0]] = gen_obj(603)		
		elif(self.id == 109): # Wooden door
			m.obj_grid[pos[1]][pos[0]] = 604
			intermap[pos[1]][pos[0]] = gen_obj(604)	
		elif(self.id == 111): # Side door
			m.obj_grid[pos[1]][pos[0]] = 114
			intermap[pos[1]][pos[0]] = gen_obj(114)	
		elif(self.id == 112): # Side door
			m.obj_grid[pos[1]][pos[0]] = 115
			intermap[pos[1]][pos[0]] = gen_obj(115)	
		elif(self.id == 113): # Side door
			m.obj_grid[pos[1]][pos[0]] = 116
			intermap[pos[1]][pos[0]] = gen_obj(116)	

class OpenDoor(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 300
		self.solid = False
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "You can open it"

	def action(self, entity, pos, m, intermap):
		if(self.id == 110): # Fancy door
			m.obj_grid[pos[1]][pos[0]] = 108
			intermap[pos[1]][pos[0]] = gen_obj(108)
		elif(self.id == 603): # Normal door
			m.obj_grid[pos[1]][pos[0]] = 107
			intermap[pos[1]][pos[0]] = gen_obj(107)		
		elif(self.id == 604): # Wooden door
			m.obj_grid[pos[1]][pos[0]] = 109
			intermap[pos[1]][pos[0]] = gen_obj(109)	
		elif(self.id == 114): # Side door
			m.obj_grid[pos[1]][pos[0]] = 111
			intermap[pos[1]][pos[0]] = gen_obj(111)	
		elif(self.id == 115): # Side door
			m.obj_grid[pos[1]][pos[0]] = 112
			intermap[pos[1]][pos[0]] = gen_obj(112)	
		elif(self.id == 116): # Side door
			m.obj_grid[pos[1]][pos[0]] = 113
			intermap[pos[1]][pos[0]] = gen_obj(113)	

class Sack(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 10
		self.solid = True
		self.transparency = True
		self.special_collision = False

	def examine(self, entity):
		return "There's something inside"

class Anvil(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 5000
		self.solid = True
		self.transparency = True
		self.special_collision = False
		
	def examine(self, entity):
		return "A heavy iron anvil for blacksmithing"

class Forge(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 4000
		self.solid = True
		self.transparency = False
		self.special_collision = False
		
	def examine(self, entity):
		return "It's scorching hot"

class OakTree(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 2000
		self.solid = True
		self.transparency = False
		self.special_collision = False
		
	def examine(self, entity):
		return "A quiet calming Oak Tree"

class PineTree(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 2000
		self.solid = True
		self.transparency = False
		self.special_collision = False

		self.add_special_collision([219,222])
		
	def examine(self, entity):
		return "A long Pine Tree"

class Cupboard(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 700
		self.solid = True
		self.transparency = False
		self.special_collision = False

		self.add_special_collision([449,432,587,427])
		
	def examine(self, entity):
		return "There are stuffed with decoration"

class Bottle(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = False
		self.hp = 5
		self.solid = False
		self.transparency = True
		self.special_collision = False
		
	def examine(self, entity):
		return "Some alcohol"

class Slider(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 1500
		self.solid = True
		self.transparency = True
		self.special_collision = False

		self.add_special_collision([251,254])
		
	def examine(self, entity):
		return "Made for kids"

class FlowerPot(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 80
		self.solid = True
		self.transparency = True
		self.special_collision = False
		
	def examine(self, entity):
		return "A beautiful plant lives here"

class Throne(GeneralObj):
	def __init__(self, id):
		self.id = id
		self.multiblock = True
		self.hp = 80
		self.solid = False
		self.transparency = True
		self.special_collision = False
		
	def examine(self, entity):
		return "Someone important seems to live here"



def get_obj_index(id):
	if(id <= 0):
		return "src\\Objects\\none.png"

	ref = open("src\\Objects\\Obj_ref", "r")
	data = ref.read()
	return "src\\Objects\\" + data.split("\n")[id] + ".png"

from ObjDictionary import *

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

