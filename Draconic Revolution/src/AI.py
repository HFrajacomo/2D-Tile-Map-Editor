from Map import *
from Pathfinding import *
from time import sleep

def easy_sum(list1, list2):
	return [list1[0]+list2[0], list1[1] + list2[1]]

class AI:
	def __init__(self, DISC_POS, OFFSET):
		self.pos = DISC_POS.copy()
		self.offset = OFFSET.copy()
		self.interrupt = "" # Triggers every odd interaction with the NPC
		self.current_action = "" # Saves last action in case of interruption
		self.speed = 1
		self.position = 0
		self.IS_MOVING = False

	###### TIER 1 MOVEMENT ######
	def step_right(self):
		self.offset[0] += self.speed
		if(self.offset[0]>=32):
			self.offset[0] = -32
			self.pos[0] += 1

		self.position = 2
	def step_left(self):
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

		while(self.pos != destination or self.offset[0] != 0):
			self.IS_MOVING = True
			self.step_left()
			if(self.interrupt != ""):
				self.IS_MOVING = False
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
		
		print(path)

		for direction in path:
			print(self.pos)
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
