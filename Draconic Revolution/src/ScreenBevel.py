import pygame as pg
from Tile import *

class ScreenBevel:
	def __init__(self, width, height, rgb, pos):
		self.fullscreen = None
		self.surf = pg.Surface((width, height))
		self.bg_color = rgb
		self.surf.fill(rgb)
		self.pos = pos
		self.rect = pg.Rect(pos, (width, height))

	def draw(self, screen):
		screen.blit(self.surf, self.pos)
		pg.display.update(self.rect)

	def update(self, screen):
		pg.display.update(pg.Rect(self.pos, self.surf.get_size()))

	def get_size(self):
		return self.surf.get_size()
	'''
	def scrollX(self, screen, dx, noupdate=False):
	    width, height = self.fullscreen.get_size()
	    copy_surf = self.fullscreen.copy()
	    self.fullscreen.fill((80,0,0))
	    self.fullscreen.blit(copy_surf, (dx, 0))
	    if dx < 0:
	    	self.fullscreen.blit(copy_surf, (width + dx, 0), (0, 0, -dx, height))
	    else:
	    	self.fullscreen.blit(copy_surf, (0, 0), (width - dx, 0, dx, height))
	    if(not noupdate):
	   		screen.blit(self.get_window([0,0]), (0,0))
	    	pg.display.update(self.rect)

	def scrollY(self, screen, dy, noupdate=False):
	    width, height = self.fullscreen.get_size()
	    copy_surf = self.fullscreen.copy()
	    self.fullscreen.fill((80,0,0))
	    self.fullscreen.blit(copy_surf, (0, dy))
	    if dy < 0:
	        self.fullscreen.blit(copy_surf, (0, height + dy), (0, 0, width, -dy))
	    else:
	        self.fullscreen.blit(copy_surf, (0, 0), (0, height - dy, width, dy))
	    if(not noupdate):
	   		screen.blit(self.get_window([0,0]), (0,0))
	    	pg.display.update(self.rect)
	'''

	# Blits the viewport
	def get_window(self, screen, discrete_pos, offset, mapsize):
		x_start = discrete_pos[0]*64 + offset[0] - 640
		y_start = discrete_pos[1]*64 + offset[1] - 448

		if(x_start < 0):
			x_start = mapsize[0] + x_start
		if(y_start < 0):
			y_start = mapsize[1] + y_start
		
		x_end = x_start + 1344
		y_end = y_start + 960



		# Viewport inside fullscreen
		if(x_start >= 0 and y_start >= 0 and x_end < mapsize[0] and y_end < mapsize[1]):
			aux = self.fullscreen.subsurface(pg.Rect((x_start, y_start), (1344, 960)))
		# Viewport going out onto x axis
		elif(x_end >= mapsize[0] and y_start >= 0 and y_end < mapsize[1]):
			x_remainder = x_end - mapsize[0] 
			aux = self.fullscreen.subsurface(pg.Rect((x_start, y_start), (1344 - x_remainder, 960)))
			aux2 = self.fullscreen.subsurface(pg.Rect((0, y_start), (x_remainder, 960)))
			screen.blit(aux2, (1344 - x_remainder, 0))
		# Viewport going out onto y axis
		elif(y_end >= mapsize[1] and x_start >= 0 and x_end < mapsize[0]):
			y_remainder = y_end - mapsize[1] 
			aux = self.fullscreen.subsurface(pg.Rect((x_start, y_start), (1344, 960 - y_remainder)))
			aux2 = self.fullscreen.subsurface(pg.Rect((x_start, 0), (1344, y_remainder)))
			screen.blit(aux2, (0, 960 - y_remainder))
		# Viewport going out onto xy
		#elif(x_end >= mapsize[0] and y_end >- mapsize[1]):
		else:
			x_remainder = x_end - mapsize[0]
			y_remainder = y_end - mapsize[1]
			aux = self.fullscreen.subsurface(pg.Rect((x_start, y_start), (1344 - x_remainder, 960 - y_remainder)))
			aux2 = self.fullscreen.subsurface(pg.Rect((0, y_start), (x_remainder, 960 - y_remainder)))
			aux3 = self.fullscreen.subsurface(pg.Rect((x_start, 0), (1344 - x_remainder, y_remainder)))

			# Fix diagonal blitting
			if(x_start >= 0):
				x_start = 0
			else:
				x_start = mapsize[0] - x_remainder
			if(y_start >= 0):
				y_start = 0
			else:
				y_start = mapsize[1] - y_remainder
		

			aux4 = self.fullscreen.subsurface(pg.Rect((x_start, y_start), (x_remainder, y_remainder)))
			
			screen.blit(aux2, (1344 - x_remainder, 0))
			screen.blit(aux3, (0, 960 - y_remainder))
			screen.blit(aux4, (1344 - x_remainder, 960 - y_remainder))			
		screen.blit(aux, (0,0))
		self.update(screen)

	# Creates fullscreen surface based on mapsize
	def load_map(self, map):
		width = len(map.grid)
		height = len(map.grid[0])
		self.fullscreen = pg.Surface(((64*width),(64*height)))

	# Builds the entire map onto fullscreen
	def build_map(self, screen, discrete_pos, map):
		tile_list = {}

		for j in range(0,len(map.grid[0])):
			for i in range(0,len(map.grid)):
				# Get all tiles that appear
				if(map.grid[i][j] not in tile_list):
					tile_list[map.grid[i][j]] = Tile(map.grid[i][j])

		for j in range(0,len(map.grid[0])):
			for i in range(0,len(map.grid)):			
				# Blitting tile mapping
				self.fullscreen.blit(tile_list[map.grid[i][j]].image, ((j*64), (i*64)))
