from Tile import Tile
from Obj import Obj

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
		sub_matrix = []
		for i in range(pos[1] - radius_y, pos[1] + radius_y+1):
			sub_matrix.append([])
			for j in range(pos[0] - radius_x, pos[0] + radius_x+1):
				try:
					if(non_circular and i<0 or j<0):
						sub_matrix[-1].append(-1)
					elif(non_circular and (i>len(self.grid)-1 or j>len(self.grid[0])-1)):
						sub_matrix[-1].append(-1)
					elif(not non_circular and i>=len(self.grid) and j>=len(self.grid[0])):
						i -= len(self.grid)
						j -= len(self.grid[0])
					elif(not non_circular and i>=len(self.grid)):
						i -= len(self.grid)
						sub_matrix[-1].append(self.grid[i][j])
					elif(not non_circular and j>=len(self.grid[0])):
						j -= len(self.grid[0])
						sub_matrix[-1].append(self.grid[i][j])
					else:
						sub_matrix[-1].append(self.grid[i][j])
				except IndexError:
					sub_matrix[-1].append(-1)
		return sub_matrix

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
