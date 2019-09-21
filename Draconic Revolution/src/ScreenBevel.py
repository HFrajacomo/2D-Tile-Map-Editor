import pygame as pg
from Tile import *
from Obj import Obj
from Light import Light
from Line import *
from TileDictionary import *
from AnimatedTilesHash import *
from AnimatedObjectHash import *
from time import sleep
from datetime import datetime
from threading import Thread, Event

class ScreenBevel:
	animated_images = {}

	def __init__(self, width, height, rgb, pos):
		
		self.width = width
		self.height = height

		self.last_animated_pos = [pos]
		self.last_animated_obj_pos = [pos, pos]

		self.fullscreen = []
		self.animated = []
		self.animated_obj = []
		self.animated.append(pg.Surface((width+1024, height+1024), pg.SRCALPHA | pg.HWSURFACE))
		self.animated_obj.append(pg.Surface((width+1024, height+1024), pg.SRCALPHA | pg.HWSURFACE))		
		self.animated_obj.append(pg.Surface((width+1024, height+1024), pg.SRCALPHA | pg.HWSURFACE))		
		self.animated[0].convert_alpha()
		self.animated_obj[0].convert_alpha()
		self.animated_obj[1].convert_alpha()

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

	# Blits the viewport
	def get_window(self, screen, discrete_pos, offset, player, mapsize, interactive_map, animation, map, LOCK):
		x_start = discrete_pos[0]*64 + offset[0] - 640
		y_start = discrete_pos[1]*64 + offset[1] - 448
		actual_flag = animation

		if(x_start < 0):
			x_start = mapsize[0] + x_start
		if(y_start < 0):
			y_start = mapsize[1] + y_start
		
		x_end = x_start + 1344
		y_end = y_start + 960

		# Viewport inside fullscreen
		if(x_start >= 0 and y_start >= 0 and x_end < mapsize[0] and y_end < mapsize[1]):
			aux = self.fullscreen[0].subsurface(pg.Rect((x_start, y_start), (1344, 960)))
			auxo = self.fullscreen[1].subsurface(pg.Rect((x_start, y_start), (1344, 960)))
		# Viewport going out onto x axis
		elif(x_end >= mapsize[0] and y_start >= 0 and y_end < mapsize[1]):
			x_remainder = x_end - mapsize[0] 
			aux = self.fullscreen[0].subsurface(pg.Rect((x_start, y_start), (1344 - x_remainder, 960)))
			aux2 = self.fullscreen[0].subsurface(pg.Rect((0, y_start), (x_remainder, 960)))
			auxo = self.fullscreen[1].subsurface(pg.Rect((x_start, y_start), (1344 - x_remainder, 960)))
			aux2o = self.fullscreen[1].subsurface(pg.Rect((0, y_start), (x_remainder, 960)))
			screen.blit(aux2, (1344 - x_remainder, 0))
			screen.blit(aux2o, (1344 - x_remainder, 0))
		# Viewport going out onto y axis
		elif(y_end >= mapsize[1] and x_start >= 0 and x_end < mapsize[0]):
			y_remainder = y_end - mapsize[1] 
			aux = self.fullscreen[0].subsurface(pg.Rect((x_start, y_start), (1344, 960 - y_remainder)))
			aux2 = self.fullscreen[0].subsurface(pg.Rect((x_start, 0), (1344, y_remainder)))
			auxo = self.fullscreen[1].subsurface(pg.Rect((x_start, y_start), (1344, 960 - y_remainder)))
			aux2o = self.fullscreen[1].subsurface(pg.Rect((x_start, 0), (1344, y_remainder)))
			screen.blit(aux2, (0, 960 - y_remainder))			
			screen.blit(aux2o, (0, 960 - y_remainder))
		# Viewport going out onto xy
		else:
			x_remainder = x_end - mapsize[0]
			y_remainder = y_end - mapsize[1]
			aux = self.fullscreen[0].subsurface(pg.Rect((x_start, y_start), (1344 - x_remainder, 960 - y_remainder)))
			aux2 = self.fullscreen[0].subsurface(pg.Rect((0, y_start), (x_remainder, 960 - y_remainder)))
			aux3 = self.fullscreen[0].subsurface(pg.Rect((x_start, 0), (1344 - x_remainder, y_remainder)))
			auxo = self.fullscreen[1].subsurface(pg.Rect((x_start, y_start), (1344 - x_remainder, 960 - y_remainder)))
			aux2o = self.fullscreen[1].subsurface(pg.Rect((0, y_start), (x_remainder, 960 - y_remainder)))
			aux3o = self.fullscreen[1].subsurface(pg.Rect((x_start, 0), (1344 - x_remainder, y_remainder)))

			# Fix diagonal blitting
			if(x_start >= 0):
				x_start = 0
			else:
				x_start = mapsize[0] - x_remainder
			if(y_start >= 0):
				y_start = 0
			else:
				y_start = mapsize[1] - y_remainder
		

			aux4 = self.fullscreen[0].subsurface(pg.Rect((x_start, y_start), (x_remainder, y_remainder)))
			aux4o = self.fullscreen[1].subsurface(pg.Rect((x_start, y_start), (x_remainder, y_remainder)))
			
			screen.blit(aux2, (1344 - x_remainder, 0))
			screen.blit(aux3, (0, 960 - y_remainder))
			screen.blit(aux4, (1344 - x_remainder, 960 - y_remainder))		
			screen.blit(aux2o, (1344 - x_remainder, 0))
			screen.blit(aux3o, (0, 960 - y_remainder))
			screen.blit(aux4o, (1344 - x_remainder, 960 - y_remainder))	

		screen.blit(aux, (0,0)) # Blits tiles

		### Animate Tiles
		
		if(actual_flag == 0):
			try:  # If animated tiles wasn't loaded yet
				x_start = (discrete_pos[0] - self.last_animated_pos[actual_flag][0])*64 + offset[0]
				y_start = (discrete_pos[1] - self.last_animated_pos[actual_flag][1])*64 + offset[1]
				x_start_obj = (discrete_pos[0] - self.last_animated_obj_pos[bool_invert(actual_flag)][0])*64 + offset[0]
				y_start_obj = (discrete_pos[1] - self.last_animated_obj_pos[bool_invert(actual_flag)][1])*64 + offset[1]
			except:
				return

			try:
				screen.blit(self.animated[actual_flag].subsurface(pg.Rect((x_start+512, y_start+512), (1344, 960))), (0,0))		
				screen.blit(self.animated_obj[actual_flag].subsurface(pg.Rect((x_start_obj+512, y_start_obj+512), (1344, 960))), (0,0))
			except ValueError:
				pass

		if(actual_flag == 1):
			try:  # If animated tiles wasn't loaded yet
				x_start = (discrete_pos[0] - self.last_animated_obj_pos[bool_invert(actual_flag)][0])*64 + offset[0]
				y_start = (discrete_pos[1] - self.last_animated_obj_pos[bool_invert(actual_flag)][1])*64 + offset[1]
			except:
				return

			try:
				screen.blit(self.animated_obj[actual_flag].subsurface(pg.Rect((x_start+512, y_start+512), (1344, 960))), (0,0))
			except ValueError:
				pass
	
		# END animation

		player.draw(screen)	# Blits player

		screen.blit(auxo, (0,0)) # Blits objects

		# Blit blind spots (PUT THIS IN A THREAD BC SLOW)
		#blind_spots = line_of_sight(discrete_pos, interactive_map)

		# Removed darkness blitting to screen
		'''
		dark = Light(180, size=32).image
		try:
			dark_off1 = Light(180, size=64).image.subsurface(pg.Rect((0,0), (abs(offset[0]), 64)))
			dark_off2 = Light(180, size=64).image.subsurface(pg.Rect((0,0), (64, abs(offset[1]))))
			dark_off3 = Light(180, size=64).image.subsurface(pg.Rect((0,0), (abs(offset[0]), abs(offset[1]))))
		except:
			pass

		for element in blind_spots:
			
			if(element[1] == 0 and offset[0] < 0):
				screen.blit(dark_off1, (0,element[0]*64-offset[1]))
			if(element[0] == 0 and offset[1] < 0):
				screen.blit(dark_off2, (element[1]*64-offset[0], 0))
			if(element[0] == 0 and element[1] == 0):
				screen.blit(dark_off3, (0, 0))	

			screen.blit(dark, (element[1]*64-offset[0], element[0]*64-offset[1]))
		'''

		self.update(screen)

	# Creates fullscreen surface based on mapsize
	def load_map(self, map):
		width = len(map.grid)
		height = len(map.grid[0])
		self.fullscreen.append(pg.Surface(((64*width),(64*height)), pg.HWSURFACE)) # Tile Layer
		self.fullscreen.append(pg.Surface(((64*width),(64*height)), pg.SRCALPHA | pg.HWSURFACE)) # Object Layer
		self.fullscreen[0].convert_alpha()
		self.fullscreen[1].convert_alpha()


	# Builds the entire map onto fullscreen
	def build_map(self, screen, discrete_pos, map):
		obj_list = {}
		light_list = {}

		for j in range(0,len(map.grid[0])):
			for i in range(0,len(map.grid)):
				if(map.obj_grid[i][j] not in animated_obj_dictionary[0].keys()):
					obj_list[map.obj_grid[i][j]] = Obj(map.obj_grid[i][j]).image
				#if(map.light_grid[i][j] not in light_list):
				#	light_list[map.light_grid[i][j]] = Light(map.light_grid[i][j]).image

		for j in range(0,len(map.grid[0])):
			for i in range(0,len(map.grid)):			
				# Blitting tile mapping
				# Don't blit animated tiles
				try:
					self.fullscreen[0].blit(all_tiles_img[map.grid[i][j]], ((j*64), (i*64)))
				except KeyError:
					print("Map is corrupted or an invalid tile was found")
					exit()

				# Draws non-animated objects
				if(map.obj_grid[i][j] > 0 and map.obj_grid[i][j] not in animated_obj_dictionary[0].keys()):
					self.fullscreen[1].blit(obj_list[map.obj_grid[i][j]], ((j*64), (i*64)))
				#self.fullscreen[1].blit(light_list[map.light_grid[i][j]], ((j*64), (i*64)))

	# Builds a semi surface for animated tiles to be blittted over fullscreen
	def build_animated_map(self, discrete_pos, map, flag):
		if(flag == 1):
			return

		# Only redraws after moved a certain amount
		if(abs(self.last_animated_pos[int(flag)][0] - discrete_pos[0]) + abs(self.last_animated_pos[int(flag)][1] - discrete_pos[1]) < 3):
			return

		matrix = map.get_submatrix(map.grid, discrete_pos, 18, 15, non_circular=False)

		k = 0
		l = 0
		new_surf = pg.Surface((self.width+1024, self.height+1024), pg.SRCALPHA | pg.HWSURFACE)

		if(not flag):
			# Animated Tiles
			for j in range(0, 37):
				for i in range(0, 31):
					if(animated_dictionary[0].get(matrix[i][j], False) != False):
						new_surf.blit(animated_dictionary[0][matrix[i][j]].image, (k*64, l*64))
					l += 1
				k += 1
				l=0				
			
		self.animated[0] = new_surf

		self.last_animated_pos[int(flag)] = discrete_pos.copy()

	# Builds a semi surface for animated objects to be blittted over fullscreen
	def build_animated_obj_map(self, discrete_pos, map, flag):
		# Only redraws after moved a certain amount
		if(abs(self.last_animated_obj_pos[flag][0] - discrete_pos[0]) + abs(self.last_animated_obj_pos[flag][1] - discrete_pos[1]) < 4):
			return

		matrix_obj = map.get_submatrix(map.obj_grid, discrete_pos, 18, 15, non_circular=False)
		new_surf_obj = pg.Surface((self.width+1024, self.height+1024), pg.SRCALPHA | pg.HWSURFACE)

		# Animated Objects
		k = 0
		l = 0

		if(flag == 0):
			for j in range(0, 37):
				for i in range(0, 31):
					if(animated_obj_dictionary[1].get(matrix_obj[i][j], False) != False):
						new_surf_obj.blit(animated_obj_dictionary[1][matrix_obj[i][j]].image, (k*64, l*64))
					l += 1
				k += 1
				l=0	
			self.animated_obj[1] = new_surf_obj

		elif(flag == 1):
			for j in range(0, 37):
				for i in range(0, 31):
					if(animated_obj_dictionary[0].get(matrix_obj[i][j], False) != False):
						new_surf_obj.blit(animated_obj_dictionary[0][matrix_obj[i][j]].image, (k*64, l*64))
					l += 1
				k += 1
				l=0	
			self.animated_obj[0] = new_surf_obj

		self.last_animated_obj_pos[flag] = discrete_pos.copy()

def get_region(m, player_pos):
	x_start = player_pos[1]-7
	y_start = player_pos[0]-10
	matrix = []
	breaker = False
	breaker_index = 0

	for i in range(x_start, x_start+15):
		matrix.append([])
		for j in range(y_start, y_start+21):
			try:
				matrix[-1].append(m[i][j])
			except IndexError:
				breaker = True
				breaker_index = i
				break
		if(breaker):
			break

	if(breaker):
		for i in range(0, x_start+15-breaker_index-1):
			matrix.append([])
			for j in range(y_start, y_start+21):
				matrix[-1].append(m[i][j])

	return matrix

def bool_invert(num):
	if(num == 1):
		return 0
	else:
		return 1
