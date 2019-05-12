from Tile import Tile
from Map import Map
import pygame as pg
from time import sleep
from threading import Thread

class TiledMap():
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

	def __getitem__(self, i):
		return self.map_.grid[i]

	# Ctrl + Z function. Changes back to undomap
	def undo_map(self):
		if(self.undomap == None):
			return
		self.map_ = Map(None, oldmap=self.undomap)
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
	def set_map_value(self, pos_list, val):
		self.undomap = Map(None, oldmap=self.map_)

		for pos in pos_list:
			try:
				if(self.map_.grid[pos[0]+self.win_cord[0]][pos[1]+self.win_cord[1]] == val):
					continue
			except:
				continue

			self.map_.grid[pos[0]+self.win_cord[0]][pos[1]+self.win_cord[1]] = val
			self.map_.draw_grid[pos[0]+self.win_cord[0]][pos[1]+self.win_cord[1]] = True
			self.needs_draw = True

	# Draws all blits to screen all grid
	def draw_all(self, screen, pos=[0,0], size=32):
		for i in range(self.win_cord[1],self.win_cord[1]+27):
			for j in range(self.win_cord[0],self.win_cord[0]+60):
				self.bev_.surf.blit(Tile(self.map_.grid[i][j]).image, (j*size, i*size))
		self.map_.gen_draw_grid(val=False)
		self.needs_draw = False
		screen.blit(self.bev_.surf, pos)

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
	def update_tiles(self, screen, size=32, draw_grid=False):
		threads = []
		if(not self.needs_draw):
			return
		for i in range(self.win_cord[1], self.win_cord[1]+27):
			threads.append(Thread(target=self.update_row, args=(screen, i, True)))
			threads[-1].start()
			threads.append(Thread(target=self.update_row, args=(screen, i, False)))
			threads[-1].start()

		for th in threads:
			th.join()

		if(draw_grid):
			self.draw_grid(screen)
		pg.display.flip()

	# Multi-threaded accelerated function
	def update_row(self, screen, i, direc, size=32):
		if(direc):
			for j in range(self.win_cord[0],self.win_cord[0]+30):
				if(self.map_.draw_grid[i][j]):
					self.map_.draw_grid[i][j] = False
					screen.blit(Tile(self.map_.grid[i][j]).image, (j*size, i*size))
		else:
			for j in range(self.win_cord[0]+59,self.win_cord[0]-1,-1):
				if(self.map_.draw_grid[i][j]):
					self.map_.draw_grid[i][j] = False
					screen.blit(Tile(self.map_.grid[i][j]).image, (j*size, i*size))