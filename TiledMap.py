from Tile import Tile
import pygame as pg
from threading import Thread

class TiledMap():
	map_ = ""  # Sub-map for Tiled Window
	undomap = None # Ctrl + Z Accessed
	bev_ = ""  # Bevel object of the Tiled Window
	needs_draw = True

	def __init__(self, bevel, map_obj):
		self.bev_ = bevel
		self.map_ = map_obj
		self.needs_draw = True

	def __getitem__(self, i):
		return self.map_.grid[i]

	def update_map(self, new_map):
		self.map_ = new_map
		self.needs_draw = True

	def set_map_value(self, pos, val):
		if(self.map_.grid[pos[0]][pos[1]] == val):
			return
		self.map_.grid[pos[0]][pos[1]] = val
		self.map_.draw_grid[pos[0]][pos[1]] = True
		self.needs_draw = True

	def draw_all(self, screen, pos=[0,0], size=32):
		for i in range(0,len(self.map_.grid)):
			for j in range(0,len(self.map_.grid[i])):
				self.bev_.surf.blit(Tile(self.map_.grid[i][j]).image, (j*size, i*size))
		self.map_.gen_draw_grid(val=False)
		self.needs_draw = False
		screen.blit(self.bev_.surf, pos)

	def draw_grid(self, screen, pos=[0,0], size=32):
		for i in range(0, self.bev_.surf.get_width(), size):
			pg.draw.line(self.bev_.surf, pg.Color(200,200,200,255), (i,0), (i,self.bev_.surf.get_height()))
		for j in range(0, self.bev_.surf.get_height(), size):
			pg.draw.line(self.bev_.surf, pg.Color(200,200,200,255), (0,j), (self.bev_.surf.get_width(),j))
		screen.blit(self.bev_.surf, pos)

	def update_tiles(self, screen, size=32):
		threads = []
		if(not self.needs_draw):
			return
		for i in range(0,len(self.map_.grid)):
			threads.append(Thread(target=self.update_row, args=(screen, i, True)))
			threads[-1].start()
			threads.append(Thread(target=self.update_row, args=(screen, i, False)))
			threads[-1].start()

		for th in threads:
			th.join()
		pg.display.flip()

	# Multi-threaded accelerated function
	def update_row(self, screen, i, direc, size=32):
		if(direc):
			for j in range(0,int(len(self.map_.grid[0])/2)):
				if(self.map_.draw_grid[i][j]):
					self.map_.draw_grid[i][j] = False
					screen.blit(Tile(self.map_.grid[i][j]).image, (j*size, i*size))
		else:
			for j in range(len(self.map_.grid[0])-1,-1,-1):
				if(self.map_.draw_grid[i][j]):
					self.map_.draw_grid[i][j] = False
					screen.blit(Tile(self.map_.grid[i][j]).image, (j*size, i*size))