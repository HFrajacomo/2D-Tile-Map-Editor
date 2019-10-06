import pyglet as pg
from pyglet.gl import *
from pyglet.image.codecs.png import PNGImageDecoder
from Pathfinding import *
from threading import Lock
from Map import *
import random as rd


def easy_sum(l1, l2):
	return [l1[0]+l2[0], l1[1]+l2[1]]


class Player:
	def __init__(self, DP, OFFSET, filename, server=False):
		### Image works
		self.id = 0
		self.filename = filename

		if(not server):
			self.img = pg.image.load(self.filename)
			self.img = pg.image.ImageGrid(self.img, 4,3, item_width=64, item_height=64)
			self.img = pg.image.TextureGrid(self.img)
			self.animation = [pg.image.Animation.from_image_sequence(self.img[1:3], 0.3, loop=True), 
			pg.image.Animation.from_image_sequence(self.img[3:6], 0.3, loop=True),
			pg.image.Animation.from_image_sequence(self.img[6:9], 0.3, loop=True),
			pg.image.Animation.from_image_sequence(self.img[9:12], 0.3, loop=True)]
			self.movingframe = [pg.sprite.Sprite(self.animation[0], x=704, y=570), pg.sprite.Sprite(self.animation[3], x=704, y=570),
				pg.sprite.Sprite(self.animation[1], x=704, y=570), pg.sprite.Sprite(self.animation[2], x=704, y=570)]
			self.stillframe = [pg.sprite.Sprite(self.img[0], x=704, y=570), pg.sprite.Sprite(self.img[9], x=704, y=570), 
				pg.sprite.Sprite(self.img[3], x=704, y=570), pg.sprite.Sprite(self.img[6], x=704, y=570)]

			del self.animation
			del self.img	

		self.direction = 1
		self.pos = DP.copy()
		self.offset = OFFSET.copy()
		self.IS_MOVING = False
		self.interrupt = "" # Triggers every odd interaction with the NPC
		self.current_action = "" # current action
		self.speed = 8

		# AI queues
		self.action_queue = []  # Low level actions
		self.command_queue = [] # Mid Level actions
		self.high_queue = []  # High level actions
		self.wait_timer = 0

	def __str__(self):
		return f"{self.pos[0]},{self.pos[1]};{self.offset[0]},{self.offset[1]};{self.filename}"

	# Checks if entity is 50 blocks away from the player or not
	def is_in_entity_layer(self, DISC_POS):
		self.distance_from_player = abs(self.pos[0] - DISC_POS[0]) + abs(self.pos[1] - DISC_POS[1])
		if(self.distance_from_player <= 50):
			return True
		else:
			return False

	def get_total_x(self):
		return self.pos[0]*64 + self.offset[0]

	def get_total_y(self):
		return self.pos[1]*64 + self.offset[1]

	def draw(self, DISC_POS, OFFSET):

		# If is not moving
		if(not self.IS_MOVING):
			if(self.direction == 0):
				self.stillframe[0].draw()
			elif(self.direction == 1):
				self.stillframe[1].draw()
			elif(self.direction == 2):
				self.stillframe[2].draw()
			elif(self.direction == 3):
				self.stillframe[3].draw()

		# If is moving
		else:
			if(self.direction == 0):
				self.movingframe[0].draw()
			elif(self.direction == 1):
				self.movingframe[1].draw()
			elif(self.direction == 2):
				self.movingframe[2].draw()
			elif(self.direction == 3):
				self.movingframe[3].draw()		

		
	###### TIER 1 MOVEMENT ######
	def step_right(self):
		self.offset[0] += self.speed
		if(self.offset[0]>=32):
			self.offset[0] = -32
			self.pos[0] += 1
	def step_left(self):
		self.offset[0] -= self.speed	
		if(self.offset[0]<-32):
			self.offset[0] = 32
			self.pos[0] -= 1
	def step_up(self):
		self.offset[1] -= self.speed	
		if(self.offset[1]<-32):
			self.offset[1] = 32
			self.pos[1] -= 1
	def step_down(self):
		self.offset[1] += self.speed	
		if(self.offset[1]>=32):
			self.offset[1] = -32
			self.pos[1] += 1

	###### TIER 2 MOVEMENT ######
	def add_mv_right(self):
		self.command_queue.append("Move Right")
	def add_mv_left(self):
		self.command_queue.append("Move Left")
	def add_mv_up(self):
		self.command_queue.append("Move Up")
	def add_mv_down(self):
		self.command_queue.append("Move Down")

	def move_right(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)
		self.direction = 2

		if(surroundings[1][2].solid): # If can't move
			return False
		if(surroundings_obj[1][2].solid): # If can't move
			return False

		self.IS_MOVING = True
		for i in range(int(64/self.speed)):
			self.action_queue.append("R")
		self.action_queue.append("MIDH")

	def move_left(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)
		self.direction = 3

		if(surroundings[1][0].solid): # If can't move
			return False
		if(surroundings_obj[1][0].solid): # If can't move
			return False

		self.IS_MOVING = True
		for i in range(int(64/self.speed)):
			self.action_queue.append("L")
		self.action_queue.append("MIDH")

	def move_up(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)
		self.direction = 0

		if(surroundings[0][1].solid): # If can't move
			return False
		if(surroundings_obj[0][1].solid): # If can't move
			return False

		self.IS_MOVING = True
		for i in range(int(64/self.speed)):
			self.action_queue.append("U")
		self.action_queue.append("MIDV")

	def move_down(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)
		self.direction = 1

		if(surroundings[2][1].solid): # If can't move
			return False
		if(surroundings_obj[2][1].solid): # If can't move
			return False

		self.IS_MOVING = True
		for i in range(int(64/self.speed)):
			self.action_queue.append("D")
		self.action_queue.append("MIDV")

	##### TIER 3 MOVEMENT #######
	# Adds move to command to either high level queue end (append) or beginning (insert)
	def add_mv_to(self, pos, append=True):
		if(append):
			self.high_queue.append("Move to:" + str(pos[0]) + "," + str(pos[1]))
			self.high_queue.append("Moving to:" + str(pos[0]) + "," + str(pos[1]))
		else:
			self.high_queue.insert(0, "Move to:" + str(pos[0]) + "," + str(pos[1]))
			self.high_queue.insert(1, "Moving to:" + str(pos[0]) + "," + str(pos[1]))

	def move_to(self, pos, intermap, intermap_obj):
		if(intermap[pos[1]][pos[0]].solid or intermap_obj[pos[1]][pos[0]].solid):
			return False

		path = AStarSearch(intermap, intermap_obj, self.pos, pos)

		for direction in path:
			if(direction == "U"):
				self.command_queue.append("Move Up")
			elif(direction == "D"):
				self.command_queue.append("Move Down")
			elif(direction == "L"):
				self.command_queue.append("Move Left")
			elif(direction == "R"):
				self.command_queue.append("Move Right")

	###### TIER 4 CALLS ########
	# Waits fixed seconds + random()*variant
	def add_wait(self, ticks):
		self.wait_timer = ticks

	# Add wait command to high_level queue
	def add_highlevel_wait(self, fixed_seconds, variant_seconds):
		wait_time = fixed_seconds*60 + int(rd.random()*30)*variant_seconds		
		self.high_queue.append("Wait," + str(wait_time))	

	# Walks around a pos
	# INFINITE ACTION UNLESS INTERRUPTED
	def wander(self, pos, radius, hurry):
		wait_time = hurry*60 + int(rd.random()*30)*hurry
		walk_x = pos[0] + rd.randint(-radius,radius)
		walk_y = pos[1] + rd.randint(-radius,radius)

		self.add_mv_to([walk_x, walk_y], append=False)
		self.high_queue.insert(2, "Wait," + str(wait_time))
		self.high_queue.insert(3, "Wander;" + str(pos) + ";" + str(radius) + ";" + str(hurry))

	def add_wander(self, pos, radius, hurry):
		self.high_queue.append("Wander;" + str(pos) + ";" + str(radius) + ";" + str(hurry))

	def run(self, Non, intermap, intermap_obj):
		if(self.action_queue != []):
			action = self.action_queue.pop(0)

			if(action == "L"):
				self.step_left()
			elif(action == "R"):
				self.step_right()			
			elif(action == "U"):
				self.step_up()	
			elif(action == "D"):
				self.step_down()	
			elif(action == "MIDV"):
				self.offset[1] = 0
			elif(action == "MIDH"):
				self.offset[0] = 0
			elif(action == "W"):
				self.wait_timer -= 1
				if(self.wait_timer > 0):
					self.action_queue.append("W")

		elif(self.command_queue != []):
			command = self.command_queue.pop(0)

			if(command == "Move Left"):
				self.move_left(intermap, intermap_obj)
			elif(command == "Move Right"):
				self.move_right(intermap, intermap_obj)
			elif(command == "Move Up"):
				self.move_up(intermap, intermap_obj)
			elif(command == "Move Down"):
				self.move_down(intermap, intermap_obj)

		elif(self.high_queue != []):
			high_command = self.high_queue.pop(0)

			if(high_command[0:7] == "Move to"):
				pos = [int(high_command[8:].split(",")[0]), int(high_command[8:].split(",")[1])]
				self.move_to(pos, intermap, intermap_obj)
			elif(high_command[0:9] == "Moving to"):
				self.IS_MOVING = False
			elif(high_command[0:4] == "Wait"):
				wait_time = int(high_command.split(",")[1])
				self.wait_timer = wait_time
				self.action_queue.append("W")
			elif(high_command[0:6] == "Wander"):
				pos = [int(high_command.split("[")[1].split(",")[0]), int(high_command.split("]")[0].split(",")[1])]
				rad = int(high_command.split(";")[2])
				hurry = int(high_command.split(";")[3])
				self.wander(pos, rad, hurry)
		else:
			self.IS_MOVING = False

