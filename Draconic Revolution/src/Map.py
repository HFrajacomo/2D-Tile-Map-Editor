from Tile import Tile
from Obj import Obj
from AnimatedTilesHash import *

class Map:
	grid = []
	obj_grid = []
	draw_grid = []
	light_grid = []
	name = ""

	def __init__(self, mapdata, objdata, lightdata, mapname="", oldmap=None):
		# Standard construction
		if(oldmap == None):
			self.name = mapname

			# Tile_grid
			if(len(mapdata) < 27 or len(mapdata[0]) < 61):
				new_grid =  self.get_submatrix(mapdata, [0,0], 30, 13)
				self.grid = new_grid
			else:
				self.grid = mapdata
	
			# Obj_grid
			if(len(objdata) < 27 or len(objdata[0]) < 61):
				new_grid =  self.get_submatrix(objdata, [0,0], 30, 13)
				self.obj_grid = new_grid
			else:
				self.obj_grid = objdata

			# Light_grid
			if(len(lightdata) < 27 or len(lightdata[0]) < 61):
				new_grid =  self.get_submatrix(lightdata, [0,0], 30, 13)
				self.light_grid = new_grid
			else:
				self.light_grid = lightdata

			self.gen_draw_grid()

		# Copy via an older map
		else:
			self.name = oldmap.name
			self.grid = [x[:] for x in oldmap.grid]
			self.obj_grid = [x[:] for x in oldmap.obj_grid]
			self.light_grid = [x[:] for x in oldmap.light_grid]
			self.draw_grid = [x[:] for x in oldmap.draw_grid]

	# Generates draw_grid matrix
	def gen_draw_grid(self, val=True):
		self.draw_grid = []
		for i in range(0,len(self.grid)):
			self.draw_grid.append([])
			for j in range(0,len(self.grid[0])):
				self.draw_grid[-1].append(val)

	# Returns a submatrix of map.grid
	# non_circular changes to filling with -1 and rolling around map
	def get_region(self, pos, radius_x, radius_y, non_circular=True):
		sub_grid = []
		sub_obj = []
		sub_light = []
		for i in range(pos[1] - radius_y, pos[1] + radius_y+1):
			sub_grid.append([])
			sub_obj.append([])
			sub_light.append([])
			for j in range(pos[0] - radius_x, pos[0] + radius_x+1):
				try:
					if((non_circular) and (i<0 or j<0)):
						sub_grid[-1].append(-1)
						sub_obj[-1].append(0)
						sub_light[-1].append(0)
					elif((non_circular) and ((i>len(self.grid)-1 or j>len(self.grid[0])-1))):
						sub_grid[-1].append(-1)
						sub_obj[-1].append(0)
						sub_light[-1].append(0)
					elif(not non_circular and i>=len(self.grid) and j>=len(self.grid[0])):
						l = i - len(self.grid)
						m = j - len(self.grid[0])
						sub_grid[-1].append(self.grid[l][m])
						sub_obj[-1].append(self.obj_grid[l][m])
						sub_light[-1].append(self.light_grid[l][m])	
					elif(not non_circular and i>=len(self.grid)):
						l = i - len(self.grid)
						sub_grid[-1].append(self.grid[l][j])
						sub_obj[-1].append(self.obj_grid[l][j])
						sub_light[-1].append(self.light_grid[l][j])
					elif(not non_circular and j>=len(self.grid[0])):
						l = j - len(self.grid[0])
						sub_grid[-1].append(self.grid[i][l])
						sub_obj[-1].append(self.obj_grid[i][l])
						sub_light[-1].append(self.light_grid[i][l])					
					else:
						sub_grid[-1].append(self.grid[i][j])
						sub_obj[-1].append(self.obj_grid[i][j])
						sub_light[-1].append(self.light_grid[i][j])	
				except IndexError:
						sub_grid[-1].append(-1)
						sub_obj[-1].append(0)
						sub_light[-1].append(0)
		return [sub_grid, sub_obj, sub_light]

	# Formatted print for map.grid
	def quick_print(self):
		for i in range(0, len(self.grid)):
			for j in range(0, len(self.grid[i])):
				print("{:3}".format(self.grid[i][j]), end="")
			print()

	''' Draw tile to grid bevel '''
	# bevel = screen to be blitted
	# pos = bevel position
	# size = tile size
	def draw_tiles(self, bevel, pos, size=32):
		for i in range(0,len(self.grid)):
			for j in range(0,len(self.grid[i])):
				bevel.surf.blit(Tile(self.grid[i][j]).image, (j*size, i*size))
				bevel.surf.blit(Obj(self.obj_grid[i][j].image, (j*size, i*size)))

	# Returns submatrix of a given matrix
	def get_submatrix(self, matrix, pos, radius_x, radius_y, non_circular=True):
		sub_matrix = []
		for i in range(pos[1] - radius_y, pos[1] + radius_y+1):
			sub_matrix.append([])
			for j in range(pos[0] - radius_x, pos[0] + radius_x+1):
				try:
					if(non_circular and i<0 or j<0):
						sub_matrix[-1].append(-1)
					elif(non_circular and (i>len(matrix)-1 or j>len(matrix[0])-1)):
						sub_matrix[-1].append(-1)
					elif(not non_circular and i>=len(matrix) and j>=len(matrix[0])):
						i -= len(matrix)
						j -= len(matrix[0])
					elif(not non_circular and i>=len(matrix)):
						i -= len(matrix)
						sub_matrix[-1].append(matrix[i][j])
					elif(not non_circular and j>=len(matrix[0])):
						j -= len(matrix[0])
						sub_matrix[-1].append(matrix[i][j])
					else:
						sub_matrix[-1].append(matrix[i][j])
				except IndexError:
					sub_matrix[-1].append(-1)
		return sub_matrix

	# Returns whether to build animated tile screen or not
	def need_to_draw_animation(self, disc_pos):
		matrix = self.get_submatrix(self.grid, disc_pos, 18, 15, False)
		for i in range(0,31):
			for j in range(0,37):
				if(matrix[i][j] in animated_dictionary[0].keys()):
					return True

		return False  

	# Returns mapsize in pixels
	def get_pixel_size(self):
		return [len(self.grid)*64, len(self.grid[0])*64]

	# Returns mapsize in discrete
	def get_size(self):
		return [len(self.grid), len(self.grid[0])]