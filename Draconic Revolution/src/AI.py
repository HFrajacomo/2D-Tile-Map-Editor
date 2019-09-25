from Map import *
from Pathfinding import *

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
	def step_left(self):
		self.offset[0] -= self.speed	
	def step_up(self):
		self.offset[1] -= self.speed
	def step_down(self):
		self.offset[1] += self.speed	


	###### TIER 2 MOVEMENT ######
	def move_right(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		surroundings_obj = get_submatrix(intermap_obj, self.pos, 1, 1, non_circular=False)

		if(surroundings[1][2].solid): # If can't move
			return False
		if(surroundings_obj[1][2].solid): # If can't move
			return False

		destination = easy_sum(self.pos, [1,0])

		while(self.pos != destination):
			self.IS_MOVING = True
			self.step_right()
			if(self.interrupt != ""):
				self.IS_MOVING = False
				return False
		self.IS_MOVING = False
		return True

	def move_left(self, intermap, intermap_obj):
		surroundings = get_submatrix(intermap, self.pos, 1, 1, non_circular=False)
		if(surroundings[1][0].solid): # If can't move
			return False

		destination = easy_sum(self.pos, [-1,0])

		while(self.pos != destination):
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

		if(surroundings[1][0].solid): # If can't move
			return False
		if(surroundings_obj[1][0].solid): # If can't move
			return False

		destination = easy_sum(self.pos, [0,-1])

		while(self.pos != destination):
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

		while(self.pos != destination):
			self.IS_MOVING = True
			self.step_down()
			if(self.interrupt != ""):
				self.IS_MOVING = False
				return False
		self.IS_MOVING = False
		return True


	##### TIER 3 MOVEMENT #######
	def move_to(self, pos, map, intermap, intermap_obj):
		if(intermap[pos[0]][pos[1]].solid or intermap_obj[pos[0]][pos[1]].solid):
			return False

		self.current_action = "Move_to;" + str(pos[0]) + "," + str(pos[1])
		path = a_star_search(map, self.pos, pos)

		for direction in path:
			if(direction == "U"):
				self.move_up(intermap, intermap_obj)
			elif(direction == "D"):
				self.move_down(intermap, intermap_obj)
			elif(direction == "L"):
				self.move_left(intermap, intermap_obj)
			elif(direction == "R"):
				self.move_right(intermap, intermap_obj)

			if(self.interrupt != ""):
					return False
