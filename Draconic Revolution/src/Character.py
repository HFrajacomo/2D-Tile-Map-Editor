import pyglet as pg
from pyglet.gl import *
from pyglet.image.codecs.png import PNGImageDecoder
from Map import *
from Pathfinding import *
from threading import Thread
from time import sleep

def easy_sum(list1, list2):
	return [list1[0]+list2[0], list1[1] + list2[1]]

class Character:

	def __init__(self, DP, OFFSET, filename):
		self.img = pg.image.load(filename)
		self.img = pg.image.ImageGrid(self.img, 4,3, item_width=64, item_height=64)
		self.img = pg.image.TextureGrid(self.img)		
		self.animation = [pg.image.Animation.from_image_sequence(self.img[1:3], 0.3, loop=True), 
		pg.image.Animation.from_image_sequence(self.img[3:6], 0.3, loop=True),
		pg.image.Animation.from_image_sequence(self.img[6:9], 0.3, loop=True),
		pg.image.Animation.from_image_sequence(self.img[9:12], 0.3, loop=True)]
		self.movingframe = [pg.sprite.Sprite(self.animation[0]), pg.sprite.Sprite(self.animation[3]),
			pg.sprite.Sprite(self.animation[1]), pg.sprite.Sprite(self.animation[2])]
		self.stillframe = [pg.sprite.Sprite(self.img[0]), pg.sprite.Sprite(self.img[9]), 
			pg.sprite.Sprite(self.img[3]), pg.sprite.Sprite(self.img[6])]

		del self.animation
		del self.img

		self.timer = pg.clock.Clock()

		self.direction = 1
		self.pos = DP.copy()
		self.offset = OFFSET.copy()
		self.IS_MOVING = False
		self.interrupt = "" # Triggers every odd interaction with the NPC
		self.current_action = "" # Saves last action in case of interruption
		self.speed = 1



	def get_total_x(self):
		return self.pos[0]*64 + self.offset[0]

	def get_total_y(self):
		return self.pos[1]*64 + self.offset[1]

	def draw(self, DISC_POS, OFFSET):
		total_x = DISC_POS[0]*64 + OFFSET[0] - 704
		total_y = DISC_POS[1]*64 + OFFSET[1] + 568

		draw_pos = [self.get_total_x() - total_x, total_y - self.get_total_y()]

		# If is not moving
		
		if(not self.IS_MOVING):
			if(self.direction == 0):
				self.stillframe[0].x = draw_pos[0]
				self.stillframe[0].y = draw_pos[1]
				self.stillframe[0].draw()
			elif(self.direction == 1):
				self.stillframe[1].x = draw_pos[0]
				self.stillframe[1].y = draw_pos[1]
				self.stillframe[1].draw()
			elif(self.direction == 2):
				self.stillframe[2].x = draw_pos[0]
				self.stillframe[2].y = draw_pos[1]
				self.stillframe[2].draw()
			elif(self.direction == 3):
				self.stillframe[3].x = draw_pos[0]
				self.stillframe[3].y = draw_pos[1]
				self.stillframe[3].draw()

		# If is moving
		else:
			if(self.direction == 0):
				self.movingframe[0].x = draw_pos[0]
				self.movingframe[0].y = draw_pos[1]
				self.movingframe[0].draw()
			elif(self.direction == 1):
				self.movingframe[1].x = draw_pos[0]
				self.movingframe[1].y = draw_pos[1]
				self.movingframe[1].draw()
			elif(self.direction == 2):
				self.movingframe[2].x = draw_pos[0]
				self.movingframe[2].y = draw_pos[1]
				self.movingframe[2].draw()
			elif(self.direction == 3):
				self.movingframe[3].x = draw_pos[0]
				self.movingframe[3].y = draw_pos[1]
				self.movingframe[3].draw()		

		
	###### TIER 1 MOVEMENT ######
	def step_right(self):
		self.offset[0] += self.speed
		if(self.offset[0]>=32):
			self.offset[0] = -32
			self.pos[0] += 1
		self.position = 2
	def step_left(self, a):
		self.offset[0] -= self.speed	
		if(self.offset[0]<-32):
			self.offset[0] = 32
			self.pos[0] -= 1
		self.position = 3
	def step_up(self):
		self.offset[1] -= self.speed	
		if(self.offset[1]<-32):
			self.offset[1] = 32
			self.pos[1] -= 1
		self.position = 0
	def step_down(self):
		self.offset[1] += self.speed	
		if(self.offset[1]>=32):
			self.offset[1] = -32
			self.pos[1] += 1
		self.position = 1

	###### TIER 2 MOVEMENT ######
	def move_right(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)

		if(surroundings[1][2].solid): # If can't move
			return False
		if(surroundings_obj[1][2].solid): # If can't move
			return False

		destination = easy_sum(self.pos, [1,0])

		while(self.pos != destination or self.offset[0] != 0):
			self.IS_MOVING = True
			self.step_right()
			if(self.interrupt != ""):
				self.IS_MOVING = False
				return False
		self.IS_MOVING = False
		return True

	def move_left(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)

		if(surroundings[1][0].solid): # If can't move
			return False
		if(surroundings_obj[1][0].solid): # If can't move
			return False

		destination = easy_sum(self.pos, [-1,0])
		if(self.pos == destination):
			return True

		while(self.pos != destination or self.offset[0] != 0):
			self.IS_MOVING = True
			self.step_left()
			if(self.interrupt != ""):
				self.IS_MOVING = False
				NPC.timer.unschedule(self.step_left)
				return False
		self.IS_MOVING = False
		return True		

	def move_up(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)

		if(surroundings[0][1].solid): # If can't move
			return False
		if(surroundings_obj[0][1].solid): # If can't move
			return False

		destination = easy_sum(self.pos, [0,-1])

		while(self.pos != destination or self.offset[1] != 0):
			self.IS_MOVING = True
			self.step_up()
			if(self.interrupt != ""):
				self.IS_MOVING = False
				return False
		self.IS_MOVING = False
		return True		

	def move_down(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)

		if(surroundings[2][1].solid): # If can't move
			return False
		if(surroundings_obj[2][1].solid): # If can't move
			return False

		destination = easy_sum(self.pos, [0,1])

		while(self.pos != destination or self.offset[1] != 0):
			self.IS_MOVING = True
			self.step_down()
			if(self.interrupt != ""):
				self.IS_MOVING = False
				return False
		self.IS_MOVING = False
		return True


	##### TIER 3 MOVEMENT #######
	def move_to(self, pos, intermap, intermap_obj):
		if(intermap[pos[0]][pos[1]].solid or intermap_obj[pos[0]][pos[1]].solid):
			return False


		self.current_action = "Move_to;" + str(pos[0]) + "," + str(pos[1])

		path = AStarSearch(intermap, intermap_obj, self.pos, pos)

		for direction in path:
			if(direction == "U"):
				if(not self.move_up(intermap, intermap_obj)):
					return False
			elif(direction == "D"):
				if(not self.move_down(intermap, intermap_obj)):
					return False	
			elif(direction == "L"):
				if(not self.move_left(intermap, intermap_obj)):
					return False
			elif(direction == "R"):
				if(not self.move_right(intermap, intermap_obj)):
					return False
			if(self.interrupt != ""):
				return False
