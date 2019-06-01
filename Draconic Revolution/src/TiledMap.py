from Tile import Tile
from Map import Map
import pygame as pg
from time import sleep
from threading import Thread
from Obj import Obj
from Light import Light

class TiledMap():
	surf = None
	win_cord = (0,0)
	map_ = ""  # Sub-map for Tiled Window
	undomap = None # Ctrl + Z Accessed
	bev_ = ""  # Bevel object of the Tiled Window
	needs_draw = True

	def __init__(self, bevel, map_obj):
		self.bev_ = bevel
		self.map_ = map_obj
		self.needs_draw = True
		self.win_cord = (0,0)
		self.surf = pg.Surface(((25*64),(25*64)))


	# Blits a new region.
	def build_surface(self, screen, discrete_pos, offset_pos):
		chunk_radius = 25

		print_map = self.map_.get_region(discrete_pos, chunk_radius, chunk_radius, non_circular=False)
		tile_list = {}

		for j in range(0,chunk_radius):
			for i in range(0,chunk_radius):
				# Get all tiles that appear
				if(print_map[0][i][j] not in tile_list):
					tile_list[print_map[0][i][j]] = Tile(print_map[0][i][j])

		for j in range(0,chunk_radius):
			for i in range(0,chunk_radius):				
				# Blitting tile mapping
				self.bev_.fullscreen.blit(tile_list[print_map[0][i][j]].image, ((j*64), (i*64)))
		#screen.blit(self.surf, ((-32*chunk_radius), (-32*chunk_radius)))
		screen.blit(self.bev_.fullscreen, (0, 0))

	# Moves windowed view
	def win_move(self, dx=0, dy=0):
		new_x = self.win_cord[0] + dx
		new_y = self.win_cord[1] + dy 

		if(new_x < 0):
			for i in range(new_x, 0):
				for j in range(len(self.map_.grid)):
					self.map_.grid[j].insert(0, -1)
					self.map_.obj_grid[j].insert(0, 0)
					self.map_.light_grid[j].insert(0, 0)
					self.map_.draw_grid[j].insert(0, True)
			new_x = 0

		elif(new_x >= len(self.map_.grid[0]) - 60):
			for i in range(new_x, len(self.map_.grid[0])-61, -1):
				for j in range(len(self.map_.grid)):
					self.map_.grid[j].append(-1)
					self.map_.obj_grid[j].append(0)
					self.map_.light_grid[j].append(0)
					self.map_.draw_grid[j].append(True)
			new_x = len(self.map_.grid[0])-61

		if(new_y < 0):
			for i in range(new_y, 0):
				self.map_.grid.insert(0, [])
				self.map_.obj_grid.insert(0, [])
				self.map_.light_grid.insert(0, [])
				self.map_.draw_grid.insert(0, [])
				for j in range(len(self.map_.grid[1])):
					self.map_.grid[0].append(-1)
					self.map_.obj_grid[0].append(0)
					self.map_.light_grid[0].append(0)
					self.map_.draw_grid[0].append(True)
			new_y = 0

		elif(new_y >= len(self.map_.grid)-26):
			for i in range(new_y, len(self.map_.grid)-27, -1):
				self.map_.grid.append([])
				self.map_.obj_grid.append([])
				self.map_.light_grid.append([])
				self.map_.draw_grid.append([])
				for j in range(len(self.map_.grid[1])):
					self.map_.grid[-1].append(-1)
					self.map_.obj_grid[-1].append(0)
					self.map_.light_grid[-1].append(0)
					self.map_.draw_grid[-1].append(True)
			new_y = len(self.map_.grid)-27

		self.map_.gen_draw_grid()
		self.win_cord = (new_x, new_y)
		self.needs_draw = True

	# Ctrl + Z function. Changes back to undomap
	def undo_map(self):
		if(self.undomap == None):
			return
		self.map_ = Map(None, None, None, oldmap=self.undomap)
		self.map_.gen_draw_grid()
		self.undomap = None
		self.needs_draw = True

	# Loads map from Control Button
	def load_map(self, new_map):
		self.map_ = new_map
		self.needs_draw = True
		self.map_.gen_draw_grid()

	# Set a single value of grid
	# pos_list is a list of changed positions
	def set_map_value(self, pos_list, val, tile_mode):
		self.undomap = Map(None, None, None, oldmap=self.map_)

		for pos in pos_list:
			try:
				if(tile_mode):
					if(self.map_.grid[pos[0]][pos[1]] == val):
						continue
				else:
					if(self.map_.obj_grid[pos[0]][pos[1]] == val):
						continue
			except:
				continue

			if(tile_mode):
				self.map_.grid[pos[0]][pos[1]] = val
			else:
				self.map_.obj_grid[pos[0]][pos[1]] = val
			self.map_.draw_grid[pos[0]][pos[1]] = True
			self.needs_draw = True

	# Set values of light level to light_grid
	def set_light_level(self, pos_list, val):
		self.undomap = Map(None, None, None, oldmap=self.map_)

		for pos in pos_list:
			try:
				if(self.map_.light_grid[pos[0]][pos[1]] == val):
					continue
			except:
				continue	

			self.map_.light_grid[pos[0]][pos[1]] = val	
			self.map_.draw_grid[pos[0]][pos[1]] = True
			self.needs_draw = True

	# Draws all blits to screen all grid
	def draw_all(self, screen, pos=[0,0], size=32):
		self.bev_.surf.fill((0,0,0))
		for i in range(self.win_cord[1],self.win_cord[1]+27):
			for j in range(self.win_cord[0],self.win_cord[0]+60):
				self.bev_.surf.blit(Tile(self.map_.grid[i][j]).image, (j*size, i*size))
		
		for i in range(self.win_cord[1],self.win_cord[1]+27):
			for j in range(self.win_cord[0],self.win_cord[0]+60):
				if(self.map_.obj_grid[i][j] > 0):
					self.bev_.surf.blit(Obj(self.map_.obj_grid[i][j]).image, (j*size, i*size))

		self.map_.gen_draw_grid(val=False)
		self.needs_draw = False
		screen.blit(self.bev_.surf, pos)
		self.bev_.draw(screen)
		self.bev_.update(screen)

	# Clears grid
	def clear_grid(self, screen):
		self.bev_.surf.fill(pg.Color(0,0,0,255))
		sleep(0.02)
		screen.blit(self.bev_.surf, (0,0))

		for i in range(0,len(self.map_.grid)):
			for j in range(0,len(self.map_.grid[0])):
				self.map_.draw_grid[i][j] = True

		self.update_tiles(screen)

	# Draws gridded screen
	def draw_grid(self, screen, pos=[0,0], size=32):
		for i in range(0, self.bev_.surf.get_width(), size):
			pg.draw.line(screen, pg.Color(200,200,200,255), (i,0), (i,self.bev_.surf.get_height()))
		for j in range(0, self.bev_.surf.get_height(), size):
			pg.draw.line(screen, pg.Color(200,200,200,255), (0,j), (self.bev_.surf.get_width(),j))


	# Thread control function to update changed blocks
	def update_tiles(self, screen, lightmode=False, size=32, draw_grid=False):
		threads = []
		if(not self.needs_draw):
			return
		for i in range(self.win_cord[1], self.win_cord[1]+27):
			threads.append(Thread(target=self.update_row, args=(screen, i, True, lightmode)))
			threads[-1].start()
			threads.append(Thread(target=self.update_row, args=(screen, i, False, lightmode)))
			threads[-1].start()

		for th in threads:
			th.join()

		if(draw_grid):
			self.draw_grid(screen)
		pg.display.flip()

	# Multi-threaded accelerated function
	def update_row(self, screen, i, direc, lightmode, size=32):
		new_i = i - self.win_cord[1]
		if(direc):
			k = 0
			for j in range(self.win_cord[0],self.win_cord[0]+30):
				if(self.map_.draw_grid[i][j]):
					self.map_.draw_grid[i][j] = False
					screen.blit(Tile(self.map_.grid[i][j]).image, (k*size, new_i*size))
					if(self.map_.obj_grid[i][j] != 0):
						screen.blit(Obj(self.map_.obj_grid[i][j]).image, (k*size, new_i*size))
					if(self.map_.light_grid[i][j] != 0 and lightmode):
						screen.blit(Light(self.map_.light_grid[i][j]).image, (k*size, new_i*size))
					
				k +=1
		else:
			k = 59
			for j in range(self.win_cord[0]+59,self.win_cord[0]-1,-1):
				if(self.map_.draw_grid[i][j]):
					self.map_.draw_grid[i][j] = False
					screen.blit(Tile(self.map_.grid[i][j]).image, (k*size, new_i*size))
					if(self.map_.obj_grid[i][j] != 0):
						screen.blit(Obj(self.map_.obj_grid[i][j]).image, (k*size, new_i*size))
					if(self.map_.light_grid[i][j] != 0 and lightmode):
						screen.blit(Light(self.map_.light_grid[i][j]).image, (k*size, new_i*size))

				k -=1

	# returns a subregion of tilemode matrix.
	# Start and End are grid positions
	# CTRL + C Function
	def copy(self, start, end, tilemode):

		# Handling position problems
		if(end[1] < start[1] and start[0] > end[0]):
			aux = start.copy()
			start = end.copy()
			end = aux
		elif(end[1] < start[1] and start[0] < end[0]):
			aux = start.copy()
			start = [end[1], aux[0]]
			end = [aux[1], end[0]]
		elif(end[1] < start[1]):
			aux = start.copy()
			start = end.copy()
			end = aux

		outmatrix = []

		for j in range(start[1] + self.win_cord[0], end[1]+1+self.win_cord[0]):
			outmatrix.append([])
			for i in range(start[0] + self.win_cord[1], end[0]+1+self.win_cord[1]):
				if(tilemode):
					outmatrix[-1].append(self.map_.grid[i][j])
				else:
					outmatrix[-1].append(self.map_.obj_grid[i][j])

		return outmatrix

	# Pastes Matrix in tilemode grid position
	# CTRL + V Function
	def paste(self, matrix, pos, tilemode):
		k = 0
		l = 0


		for j in range(pos[1] + self.win_cord[0], pos[1] + self.win_cord[0] + len(matrix)):
			k = 0
			for i in range(pos[0] + self.win_cord[1], pos[0] + self.win_cord[1] + len(matrix[0])):
				if(tilemode):
					try:
						self.map_.grid[i][j] = matrix[l][k]
						self.map_.draw_grid[i][j] = True
					except:
						pass
				else:
					try:
						self.map_.obj_grid[i][j] = matrix[l][k]
						self.map_.draw_grid[i][j] = True
					except:
						pass
				k += 1
			l += 1