import pyglet as pg
from pyglet.gl import *
	
## all_list_img declaration down below

####### GENERAL TILE SETTINGS

def get_tile_index(ident):
	if(ident <= 0):
		return "src\\Tiles\\none.png"

	ref = open("src\\Tiles\\Tile_ref", "r")
	data = ref.read()
	ref.close()
	return "src\\Tiles\\" + data.split("\n")[ident] + ".png"

class Tile:
	def __init__(self, ident, frame, size=32, scaling=2):
		self.size = size
		self.image = pg.image.load(get_tile_index(ident)).get_texture()
		if(scaling != 1):
			self.scale(scaling)

	def scale(self, x):
		glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)  
		self.image.width = self.size*x
		self.image.height = self.size*x


class AnimatedTile:
	def __init__(self, ident, frame, size=32, scaling=2):
		self.size = size
		self.image = None
		self.scaling = scaling
		self.image = pg.image.load(get_tile_index(ident)).get_texture()
		self.scale(scaling, frame)

	def scale(self, x, frame):
		self.image = self.image.get_region(frame*self.size,frame*self.size, self.size, self.size)
		glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)  
		self.image.width = self.image.width*x
		self.image.height = self.image.height*x


class GeneralTile:
	id = None
	def __init__(self):
		self.hp = None
		self.solid = None
		self.transparency = None
		self.work = 1

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

############

class NoneTile(GeneralTile):
	id = 0

	def __init__(self):
		self.hp = None
		self.solid = False
		self.transparency = True
		self.work = 999

	def examine(self, entity):
		return "It goes deep down"

	# def step_on

class CobbleHard(GeneralTile):
	id = 2

	def __init__(self):
		self.hp = 200
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self,entity):
		return "A dense cobblestone pathway"

class CobbleLight(GeneralTile):
	id = 3

	def __init__(self):
		self.hp = 150
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self,entity):
		return "A cobblestone pathway"

class WoodBlock(GeneralTile):
	id = 7

	def __init__(self):
		self.hp = 200
		self.solid = True
		self.transparency = False
		self.work = 9999

	def examine(self,entity):
		return "A solid wood block used in building"

	def action(self, entity):
		# If wearing axe
		pass

	def attacked(self, entity):
		# make attacked thingy
		pass

class StoneBrick(GeneralTile):
	id = 9

	def __init__(self):
		self.hp = 500
		self.solid = True
		self.transparency = False
		self.work = 9999

	def examine(self,entity):
		return "A solid stone block used in building"

	def action(self, entity):
		# If wearing pickaxe
		pass

	def attacked(self, entity):
		# make attacked /4 damage
		pass

class BasaltFloor(GeneralTile):
	id = 10

	def __init__(self):
		self.hp = 500
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self,entity):
		return "A resilient basalt pathway"

class BasaltBrick(GeneralTile):
	id = 11

	def __init__(self):
		self.hp = 1250
		self.solid = True
		self.transparency = False
		self.work = 9999

	def examine(self,entity):
		return "A solid block of basalt used in secure buildings"

	def action(self, entity):
		# If wearing pickaxe
		pass

	def attacked(self, entity):
		# make attacked /4 damage
		pass

class CheckerFloor(GeneralTile):
	id = 14

	def __init__(self):
		self.hp = 300
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self,entity):
		return "A beautifully crafted checkers floor"

class CobbleStairs(GeneralTile):
	id = 16

	def __init__(self):
		self.hp = 300
		self.solid = False
		self.transparency = True
		self.work = 2

	def examine(self,entity):
		return "Cobblestone Stairs. You climb them."

class GrassCliff(GeneralTile):
	id = 18

	def __init__(self):
		self.hp = 300
		self.solid = True
		self.transparency = True
		self.work = 9999

	def examine(self,entity):
		return "Be careful not to walk off the edge"

class Grass(GeneralTile):
	id = 20

	def __init__(self):
		self.hp = 100
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self,entity):
		return "It's just grass"

	def action(self, entity):
		# If pickaxe damage
		pass

class WoodPlank(GeneralTile):
	id = 24

	def __init__(self):
		self.hp = 100
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self,entity):
		return "Be careful not to walk off the edge"

	def action(self, entity):
		#if pickaxe
		pass

class Water(GeneralTile):
	id = 28

	def __init__(self):
		self.hp = None
		self.solid = False
		self.transparency = True
		self.work = 8

	def examine(self, entity):
		return "It's water"

	def step_on(self, entity):
		# Slows entity
		pass

class Sand(GeneralTile):
	id = 29

	def __init__(self):
		self.hp = None
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self, entity):
		return "Several thousands of sand grains together"

	def action(self, entity):
		# Picks sand and changes block to sandstone
		pass

class Dirt(GeneralTile):
	id = 30

	def __init__(self):
		self.hp = 50
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self, entity):
		return "Several thousands sand grains together"

	def action(self, entity):
		# If pickaxe
		pass

class RedCarpet(GeneralTile):
	id = 31 #[x for x in range(31,40)]

	def __init__(self):
		self.hp = 50
		self.solid = False
		self.transparency = True
		self.work = 1

	def examine(self, entity):
		return "Royal red carpet"

	def action(self, entity):
		# If pickaxe
		pass

### All tiles ###
# Animated Tiles

'''

UPDATE THIS CODELIST EVERYTIME YOU ADD A NEW ANIMATED TILE

'''
animated_codelist = [28]

# Generates Dictionary
animated_dictionary = [{},{},{}]

for element in animated_codelist:
	animated_dictionary[0][element] = AnimatedTile(element,0).image
	animated_dictionary[1][element] = AnimatedTile(element,1).image
	animated_dictionary[2][element] = AnimatedTile(element,2).image

### All tiles

all_tiles_img = {}

for i in range(-1,9999):
	try:
		if(i not in animated_dictionary[0].keys()):
			all_tiles_img[i] = Tile(i,0).image
	except IndexError:
		break
